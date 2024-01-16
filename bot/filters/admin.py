from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.users import is_admin


class AdminFilter(BaseFilter):
    """Allows only administrators (whose database column is_admin=True)."""

    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        if not message.from_user:
            return False

        user_id = message.from_user.id

        return await is_admin(session=session, user_id=user_id)
