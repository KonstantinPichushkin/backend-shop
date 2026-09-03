from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class ProductRead(BaseModel):
    id : int
    name : str
    description : str | None
    price : Decimal

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name : str
    description : str | None = None
    price : Decimal