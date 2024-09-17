from decimal import Decimal
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.receipt import ReceiptCreate, ReceiptFilter, ReceiptResponse
from app.db.main import get_db
from app.db.models.receipt import PaymentType, Product, Receipt
from app.repository.receipts import ReceiptRepository


class ReceiptService:
    def __init__(self, session: AsyncSession):
        self.repository = ReceiptRepository(session)

    async def create_receipt(
        self, user_id: int, receipt_data: ReceiptCreate
    ) -> ReceiptResponse:
        total = sum(
            product.price * product.quantity for product in receipt_data.products
        )
        rest = max(Decimal("0"), receipt_data.payment.amount - total)

        receipt = Receipt(
            user_id=user_id,
            total=total,
            payment_type=PaymentType(receipt_data.payment.type),
            payment_amount=receipt_data.payment.amount,
            rest=rest,
        )

        receipt.products = [
            Product(
                name=product.name,
                price=product.price,
                quantity=product.quantity,
                total=product.price * product.quantity,
            )
            for product in receipt_data.products
        ]

        created_receipt = await self.repository.create(receipt)
        return created_receipt

    async def get_receipt(self, receipt_id: int, user_id: int) -> Optional[Receipt]:
        receipt = await self.repository.get_by_id(receipt_id)

        if not receipt or receipt.user_id != user_id:
            return None

        return receipt

    async def get_receipt_public(self, receipt_id: int) -> Receipt:
        return await self.repository.get_by_id(receipt_id=receipt_id)

    async def get_user_receipts(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 10,
        filters: ReceiptFilter = None,
    ):
        payment_type = None
        if filters and filters.payment_type:
            try:
                payment_type = PaymentType(filters.payment_type)
            except ValueError:
                # Handle invalid payment type
                raise ValueError(f"Invalid payment type: {filters.payment_type}")

        receipts = await self.repository.get_user_receipts(
            user_id=user_id,
            skip=skip,
            limit=limit,
            start_date=filters.start_date if filters else None,
            end_date=filters.end_date if filters else None,
            min_total=filters.min_total if filters else None,
            payment_type=payment_type,
        )

        return receipts

    def render_receipt_text(self, receipt: Receipt, line_length: int = 32) -> str:
        # Header
        output = []
        output.append(f"{'FOP Johnsoniuk Borys':^{line_length}}")
        output.append("=" * line_length)

        # Products
        for product in receipt.products:
            quantity_price = f"{product.quantity} x {product.price:,.2f}"
            total_price = f"{product.total:,.2f}"
            output.append(
                f"{quantity_price:<{line_length - len(total_price)}}{total_price}"
            )
            if len(product.name) > line_length:
                # Split product name into multiple lines
                product_lines = [
                    product.name[i : i + line_length]
                    for i in range(0, len(product.name), line_length)
                ]
                output.extend(product_lines)
            else:
                output.append(f"{product.name:<{line_length}}")
            output.append("-" * line_length)

        # Totals
        output.append("=" * line_length)
        output.append(
            f"{'TOTAL':<{line_length - len(f'{receipt.total:,.2f}')}}{receipt.total:,.2f}"
        )
        output.append(
            f"{receipt.payment_type.name.capitalize():<{line_length - len(f'{receipt.payment_amount:,.2f}')}}{receipt.payment_amount:,.2f}"
        )
        output.append(
            f"{'Change':<{line_length - len(f'{receipt.rest:,.2f}')}}{receipt.rest:,.2f}"
        )
        output.append("=" * line_length)

        # Footer
        date_str = receipt.created_at.strftime("%d.%m.%Y %H:%M")
        output.append(f"{date_str:^{line_length}}")
        output.append(f"{'Thank you for your purchase!':^{line_length}}")

        # Combine all lines into a single string
        receipt_text = "\n".join(output)
        return receipt_text


async def get_receipt_service(
    session: AsyncSession = Depends(get_db),
) -> ReceiptService:
    return ReceiptService(session)
