from fastapi import FastAPI

from app.api.v1.receipts import router as receipt_router
from app.api.v1.users import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="HIRE1 TEST TASK",
        docs_url="/api/docs",
    )
    app.include_router(user_router)
    app.include_router(receipt_router)

    return app
