from app.db.config import DBConfig
from app.db.database import Database


config = DBConfig()

database = Database(url=config.full_database_url)


async def get_db():
    async with database.get_session() as session:
        yield session
