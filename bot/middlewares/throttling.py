from __future__ import annotations
from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware
from cachetools import TTLCache

from bot.core.config import settings

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from aiogram.types import Chat, TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    cache: TTLCache[int, Any]

    def __init__(self, rate_limit: float = settings.RATE_LIMIT) -> None:
        self.cache = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        chat: Chat | None = getattr(event, "chat", None)
        if not chat:
            return await handler(event, data)

        if chat.id in self.cache:
            return None
        self.cache[chat.id] = None
        return await handler(event, data)
