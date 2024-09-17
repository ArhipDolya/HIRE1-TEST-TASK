from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    price: Decimal
    quantity: Decimal


class ProductResponse(BaseModel):
    name: str
    price: Decimal
    quantity: Decimal
    total: Decimal

    model_config = ConfigDict(from_attributes=True)
