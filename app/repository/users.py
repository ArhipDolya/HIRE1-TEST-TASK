from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class BaseUserRepository(ABC):
    @abstractmethod
    async def create(
        self, username: str, email: str, hashed_password: str
    ) -> User | None:
        ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        ...

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        ...


class UserRepository(BaseUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, username: str, email: str, hashed_password: str
    ) -> User | None:
        db_user = User(username=username, email=email, hashed_password=hashed_password)
        self.session.add(db_user)

        try:
            await self.session.commit()
            await self.session.refresh(db_user)
        except IntegrityError:
            await self.session.rollback()
            return None

        return db_user

    async def get_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        query = select(User).filter(User.id == user_id)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()
