from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.i18n import gettext as _

from bot.keyboards.inline.menu import main_keyboard
from bot.services.analytics import analytics

router = Router(name="start")


@router.message(CommandStart())
@analytics.track_event("Sign Up")
async def start_handler(message: types.Message) -> None:
    """Welcome message."""
    await message.answer(_("first message"), reply_markup=main_keyboard())
