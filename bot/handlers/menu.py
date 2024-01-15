from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline.menu import main_keyboard

router = Router(name="menu")


@router.message(Command(commands=["menu", "main"]))
async def menu_handler(message: types.Message) -> None:
    """Главное меню при вызове команды."""
    await message.answer(_("title main keyboard"), reply_markup=main_keyboard())
