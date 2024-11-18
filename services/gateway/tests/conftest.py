from typing import AsyncIterator
import pytest

import asyncio

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi import FastAPI
from starlette.testclient import TestClient
from httpx import AsyncClient

from api.core.settings import APIConfig
from main import app


async_engine = create_async_engine(
    APIConfig.DATABASE_CONNECTION_URI,
    echo=True
)


# async def get_async_session() -> AsyncIterator[AsyncSession]:
#     async_session = sessionmaker(
#         bind=async_engine,
#         class_=AsyncSession,
#         expire_on_commit=False,
#         autocommit=False,
#         autoflush=False,
#     )
#     async with async_session() as session:
#         yield session


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope='session')
async def async_db_engine():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield async_engine

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope='function')
async def async_db(async_db_engine):
    async_session = sessionmaker(
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
        bind=async_db_engine,
        class_=AsyncSession,
    )

    async with async_session() as session:
        await session.begin()

        yield session

        await session.rollback()

        for table in reversed(SQLModel.metadata.sorted_tables):
            await session.execute(f'TRUNCATE {table.name} CASCADE;')
            await session.commit()


@pytest.fixture(scope='session')
async def async_client() -> AsyncClient:
    return AsyncClient(app=FastAPI(), base_url='http://localhost')

# let test session to know it is running inside event loop


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture
# async def async_example_orm(async_db: AsyncSession) -> Example:
#     example = Example(name='test', age=18, nick_name='my_nick')
#     async_db.add(example)
#     await async_db.commit()
#     await async_db.refresh(example)
#     return example
