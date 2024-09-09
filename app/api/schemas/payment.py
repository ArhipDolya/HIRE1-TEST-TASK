from pydantic import BaseModel
from decimal import Decimal

from app.api.schemas.common import PaymentType


class PaymentCreate(BaseModel):
    type: PaymentType
    amount: Decimal


class PaymentResponse(BaseModel):
    type: PaymentType
    amount: Decimal