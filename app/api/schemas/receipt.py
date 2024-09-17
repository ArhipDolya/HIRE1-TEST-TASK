from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.api.schemas.common import PaymentType
from app.api.schemas.payment import PaymentCreate, PaymentResponse
from app.api.schemas.product import ProductCreate, ProductResponse


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

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, db_receipt):
        return cls(
            id=db_receipt.id,
            products=[ProductResponse.model_validate(p) for p in db_receipt.products],
            payment=PaymentResponse(
                type=db_receipt.payment_type, amount=db_receipt.payment_amount
            ),
            total=db_receipt.total,
            rest=db_receipt.rest,
            created_at=db_receipt.created_at,
        )


class ReceiptFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    min_total: Optional[Decimal] = None
    payment_type: Optional[PaymentType] = None
