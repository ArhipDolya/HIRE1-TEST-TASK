from decimal import Decimal

from pydantic import BaseModel

from app.api.schemas.common import PaymentType


class PaymentCreate(BaseModel):
    type: PaymentType
    amount: Decimal


class PaymentResponse(BaseModel):
    type: PaymentType
    amount: Decimal
