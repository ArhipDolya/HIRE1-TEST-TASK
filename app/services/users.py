from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.user import TokenPair, UserCreate
from app.db.main import get_db
from app.db.models.user import User
from app.repository.users import UserRepository
from app.services.auth_utils import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_hashed_password,
    verify_password,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def create_user(self, user: UserCreate) -> User | None:
        hashed_password = get_hashed_password(user.password)
        return await self.repository.create(user.username, user.email, hashed_password)

    async def authenticate_user(self, username: str, password: str):
        user = await self.repository.get_by_username(username=username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def create_user_token(self, user_id: int) -> TokenPair:
        token_data = {"sub": str(user_id)}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        return TokenPair(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )

    async def refresh_tokens(self, refresh_token: str) -> TokenPair | None:
        try:
            payload = decode_token(refresh_token)
            user_id = int(payload["sub"])
            return self.create_user_token(user_id)
        except:
            return None

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_by_id(user_id=user_id)


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)
