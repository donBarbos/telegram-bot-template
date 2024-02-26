from __future__ import annotations
from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from bot.filters.admin import AdminFilter
from bot.services.users import get_all_users, get_user_count
from bot.utils.users_export import convert_users_to_csv

if TYPE_CHECKING:
    from aiogram.types import BufferedInputFile, Message
    from sqlalchemy.ext.asyncio import AsyncSession

    from bot.database.models import UserModel


router = Router(name="export_users")


@router.message(Command(commands="export_users"), AdminFilter())
async def export_users_handler(message: Message, session: AsyncSession) -> None:
    """Export all users in csv file."""
    all_users: list[UserModel] = await get_all_users(session)
    document: BufferedInputFile = await convert_users_to_csv(all_users)
    count: int = await get_user_count(session)

    await message.answer_document(document=document, caption=_("user counter: <b>{count}</b>").format(count=count))
