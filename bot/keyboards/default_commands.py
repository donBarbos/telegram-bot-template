from __future__ import annotations
from typing import TYPE_CHECKING

from aiogram.types import BotCommand, BotCommandScopeDefault

if TYPE_CHECKING:
    from aiogram import Bot

users_commands: dict[str, dict[str, str]] = {
    "en": {
        "help": "help",
        "contacts": "developer contact details",
        "menu": "main menu with earning schemes",
        "settings": "setting information about you",
        "supports": "support contacts",
    },
    "uk": {
        "help": "help",
        "contacts": "developer contact details",
        "menu": "main menu with earning schemes",
        "settings": "setting information about you",
        "supports": "support contacts",
    },
    "ru": {
        "help": "help",
        "contacts": "developer contact details",
        "menu": "main menu with earning schemes",
        "settings": "setting information about you",
        "supports": "support contacts",
    },
}

admins_commands: dict[str, dict[str, str]] = {
    **users_commands,
    "en": {
        "ping": "Check bot ping",
        "stats": "Show bot stats",
    },
    "uk": {
        "ping": "Check bot ping",
        "stats": "Show bot stats",
    },
    "ru": {
        "ping": "Check bot ping",
        "stats": "Show bot stats",
    },
}


async def set_default_commands(bot: Bot) -> None:
    await remove_default_commands(bot)

    for language_code in users_commands:
        await bot.set_my_commands(
            [
                BotCommand(command=command, description=description)
                for command, description in users_commands[language_code].items()
            ],
            scope=BotCommandScopeDefault(),
        )

        """ Commands for admins
        for admin_id in await admin_ids():
            await bot.set_my_commands(
                [
                    BotCommand(command=command, description=description)
                    for command, description in admins_commands[language_code].items()
                ],
                scope=BotCommandScopeChat(chat_id=admin_id),
            )
        """


async def remove_default_commands(bot: Bot) -> None:
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
