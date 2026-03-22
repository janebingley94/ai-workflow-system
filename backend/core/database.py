from __future__ import annotations

from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from core.config import settings


metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata


def _get_database_url() -> str:
    return settings.database_url or "postgresql+asyncpg://user:password@localhost:5432/ai_app"


def get_engine() -> AsyncEngine:
    return create_async_engine(_get_database_url(), future=True)


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(get_engine(), expire_on_commit=False)


async def init_db() -> None:
    import models.database  # noqa: F401
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        yield session
