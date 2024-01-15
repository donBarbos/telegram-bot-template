from __future__ import annotations
from typing import TYPE_CHECKING, Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramNotFound
from aiogram.methods import GetChatMember

if TYPE_CHECKING:
    from aiogram.types import Message


class ChannelSubscribeMiddleware(BaseMiddleware):
    """The middleware is only guaranteed to work for other users if the bot is an administrator in the chat."""

    def __init__(self, chat_ids: list[int | str] | int | str) -> None:
        self.chat_ids = chat_ids
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        message: Message = event

        if not message.from_user:
            return await handler(event, data)

        user_id = message.from_user.id
        bot: Bot = data["bot"]

        if await self._is_subscribed(bot=bot, user_id=user_id):
            return await handler(event, data)
        return None

        # await message.answer(_("first subscribe to this channel(s)/group(s)"), reply_markup=)

    async def _is_subscribed(self, bot: Bot, user_id: int) -> bool:
        if isinstance(self.chat_ids, list):
            for chat_id in self.chat_ids:
                try:
                    member = await bot(GetChatMember(chat_id=chat_id, user_id=user_id))
                except TelegramNotFound:
                    return False

                if member.status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED, ChatMemberStatus.RESTRICTED):
                    return False

        elif isinstance(self.chat_ids, (str, int)):
            try:
                member = await bot(GetChatMember(chat_id=self.chat_ids, user_id=user_id))
            except TelegramNotFound:
                return False

            if member.status in (ChatMemberStatus.LEFT, ChatMemberStatus.KICKED):
                return False

        return True
