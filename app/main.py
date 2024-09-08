from fastapi import FastAPI


async def create_app() -> FastAPI:
    app = FastAPI(
        title="HIRE1 TEST TASK",
    )
    
    return app
