from pydantic import BaseModel
from decimal import Decimal


class ProductCreate(BaseModel):
    name: str
    price: Decimal
    quantity: Decimal


class ProductResponse(BaseModel):
    name: str
    price: Decimal
    quantity: Decimal
    total: Decimal
