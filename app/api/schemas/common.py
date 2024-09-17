from enum import Enum


class PaymentType(str, Enum):
    CASH = "cash"
    CASHLESS = "cashless"
