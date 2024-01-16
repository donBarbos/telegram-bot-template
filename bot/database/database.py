from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import uuid4

from asyncpg import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from bot.core.config import settings
from bot.database.models import Base

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class CConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f"__asyncpg_{prefix}_{uuid4()}__"


def get_engine(url: URL | str = settings.database_url) -> AsyncEngine:
    return create_async_engine(
        url=url,
        echo=settings.DEBUG,
        pool_size=0,
        connect_args={
            "connection_class": CConnection,
        },
    )


def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def create_tables(engine: AsyncEngine) -> None:
    """Create tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


db_url = settings.database_url
engine = get_engine(url=db_url)
sessionmaker = get_sessionmaker(engine)
