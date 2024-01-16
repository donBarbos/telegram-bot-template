from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard() -> InlineKeyboardMarkup:
    """Use in main menu."""
    buttons = [
        [InlineKeyboardButton(text=_("wallet button"), callback_data="wallet")],
        [InlineKeyboardButton(text=_("premium button"), callback_data="premium")],
        [InlineKeyboardButton(text=_("info button"), callback_data="info")],
        [InlineKeyboardButton(text=_("support button"), callback_data="support")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(1, 1, 2)

    return keyboard.as_markup()
