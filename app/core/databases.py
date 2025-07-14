from collections.abc import AsyncIterator, AsyncGenerator


from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.settings import settings
from contextlib import asynccontextmanager

__all__ = ["async_engine", "async_session", "get_async_context_session", "get_async_session"]


async_engine = create_async_engine(settings.DB_URL)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

@asynccontextmanager
async def get_async_context_session() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session

async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
        await session.close()
