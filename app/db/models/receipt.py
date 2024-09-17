from enum import Enum

from sqlalchemy import CheckConstraint, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.models.base import TimedBaseModel


class PaymentType(Enum):
    CASH = "cash"
    CASHLESS = "cashless"


class Receipt(TimedBaseModel):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    total = Column(Numeric(10, 2), nullable=False)
    payment_type = Column(SQLAlchemyEnum(PaymentType), nullable=False)
    payment_amount = Column(Numeric(10, 2), nullable=False)
    rest = Column(Numeric(10, 2), nullable=False)

    user = relationship("User", back_populates="receipts")
    products = relationship(
        "Product", back_populates="receipt", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint("payment_amount >= total", name="check_payment_amount"),
        CheckConstraint("rest >= 0", name="check_rest_non_negative"),
    )

    def __repr__(self):
        return f"<Receipt(id={self.id}, user_id={self.user_id}, total={self.total})>"


class Product(TimedBaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(
        Integer,
        ForeignKey("receipts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    receipt = relationship("Receipt", back_populates="products")

    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_non_negative"),
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint("total = price * quantity", name="check_total_calculation"),
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity})>"
