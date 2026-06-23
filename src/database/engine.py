from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@asynccontextmanager
async def create_session() -> AsyncGenerator[AsyncSession, None]:
    from src.config import config

    engine: AsyncEngine | None = None
    try:
        engine = create_async_engine(
            config.db_dsn,
            pool_size=2,
            max_overflow=5,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False,
        )
        factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with factory() as session:
            yield session
    finally:
        if engine is not None:
            await engine.dispose()
