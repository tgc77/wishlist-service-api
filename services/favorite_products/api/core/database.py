from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from api.core.settings import APIConfig


DATABASE_CONNECTION_URI = str(APIConfig.DATABASE_CONNECTION_URI).format(
    DB_USERNAME=APIConfig.MYSQL_USERNAME,
    DB_PASSWORD=APIConfig.MYSQL_PASSWORD,
    DB_HOST=APIConfig.MYSQL_HOST,
    DB_PORT=APIConfig.MYSQL_PORT,
    DB_NAME=APIConfig.MYSQL_DATABASE
)

async_engine = create_async_engine(
    DATABASE_CONNECTION_URI,
    echo=True,
    future=True,
    pool_size=10,
    max_overflow=20
)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def create_database_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Table models created in database successfully")
