from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class ProductRead(BaseModel):
    id : int
    name : str
    description : str | None
    price : Decimal

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    name : str
    description : str | None = None
    price : Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class ProductUpdate(BaseModel):
    name : str | None = None
    description : str | None = None
    price : Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
