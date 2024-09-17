from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.schemas.receipt import ReceiptCreate, ReceiptFilter, ReceiptResponse
from app.db.models.user import User
from app.services.auth_dependencies import get_current_user
from app.services.receipts import ReceiptService, get_receipt_service

router = APIRouter(prefix="/api/v1/receipts")


@router.post("", response_model=ReceiptResponse)
async def create_receipt(
    receipt: ReceiptCreate,
    current_user: User = Depends(get_current_user),
    receipt_service: ReceiptService = Depends(get_receipt_service),
) -> ReceiptResponse:
    try:
        created_receipt = await receipt_service.create_receipt(
            user_id=current_user.id, receipt_data=receipt
        )
        return ReceiptResponse.from_orm(created_receipt)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@router.get("/{receipt_id}", response_model=ReceiptResponse)
async def get_receipt(
    receipt_id: int,
    current_user: User = Depends(get_current_user),
    receipt_service: ReceiptService = Depends(get_receipt_service),
):
    try:
        receipt = await receipt_service.get_receipt(receipt_id, current_user.id)

        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found"
            )

        return ReceiptResponse.from_orm(receipt)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )


@router.get("", response_model=list[ReceiptResponse])
async def get_user_receipts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=100),
    filters: ReceiptFilter = Depends(),
    current_user: User = Depends(get_current_user),
    receipt_service: ReceiptService = Depends(get_receipt_service),
):
    try:
        receipts = await receipt_service.get_user_receipts(
            user_id=current_user.id, skip=skip, limit=limit, filters=filters
        )
        return [ReceiptResponse.from_orm(receipt) for receipt in receipts]
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )


@router.get("/{receipt_id}/view", response_class=PlainTextResponse)
async def get_receipt_view(
    receipt_id: int,
    line_length: int = Query(32, gt=10, lt=100),
    receipt_service: ReceiptService = Depends(get_receipt_service),
):
    try:
        receipt = await receipt_service.get_receipt_public(receipt_id=receipt_id)

        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found"
            )

        receipt_text = receipt_service.render_receipt_text(receipt, line_length)
        return receipt_text

    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        )
