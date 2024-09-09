from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

from app.api.schemas.product import ProductCreate, ProductResponse
from app.api.schemas.payment import PaymentCreate, PaymentResponse


class ReceiptCreate(BaseModel):
    products: list[ProductCreate]
    payment: PaymentCreate


class ReceiptResponse(BaseModel):
    id: int
    products: list[ProductResponse]
    payment: PaymentResponse
    total: Decimal
    rest: Decimal
    created_at: datetime

    class Config:
        orm_mode = True
