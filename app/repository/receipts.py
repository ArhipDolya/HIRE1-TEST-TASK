from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.receipt import PaymentType, Receipt


class BaseReceiptRepository(ABC):
    @abstractmethod
    async def create(self, receipt: Receipt) -> Receipt:
        ...

    @abstractmethod
    async def get_by_id(self, receipt_id: int) -> Receipt | None:
        ...

    @abstractmethod
    async def get_user_receipts(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_total: Optional[float] = None,
        payment_type: Optional[PaymentType] = None,
    ) -> list[Receipt]:
        ...


class ReceiptRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, receipt: Receipt) -> Receipt:
        try:
            self.session.add(receipt)
            await self.session.commit()

            # Refresh the receipt with eagerly loaded products
            stmt = (
                select(Receipt)
                .options(selectinload(Receipt.products))
                .filter(Receipt.id == receipt.id)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except IntegrityError as e:
            await self.session.rollback()
            if "check_payment_amount" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid payment amount. Please check the total and payment amount values.",
                )

    async def get_by_id(self, receipt_id: int) -> Receipt | None:
        query = (
            select(Receipt)
            .options(selectinload(Receipt.products))
            .where(Receipt.id == receipt_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_receipts(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        min_total: Optional[float] = None,
        payment_type: Optional[PaymentType] = None,
    ) -> list[Receipt]:
        query = (
            select(Receipt)
            .options(selectinload(Receipt.products))
            .where(Receipt.user_id == user_id)
        )

        # Create a list to hold all filter conditions
        filters = []

        if start_date:
            filters.append(Receipt.created_at >= start_date)
        if end_date:
            filters.append(Receipt.created_at <= end_date)
        if min_total is not None:
            filters.append(Receipt.total >= min_total)
        if payment_type:
            filters.append(Receipt.payment_type == payment_type)

        # Apply all filters at once
        if filters:
            query = query.where(and_(*filters))

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)

        return result.scalars().all()
