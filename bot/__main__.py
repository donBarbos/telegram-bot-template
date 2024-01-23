from __future__ import annotations
import asyncio

import sentry_sdk
from loguru import logger
from sentry_sdk.integrations.loguru import LoggingLevels, LoguruIntegration

from bot.core.config import settings
from bot.core.loader import bot, dp
from bot.handlers import get_handlers_router
from bot.keyboards.default_commands import remove_default_commands, set_default_commands
from bot.middlewares import register_middlewares


async def startup() -> None:
    logger.info("bot starting...")

    register_middlewares(dp)

    dp.include_router(get_handlers_router())

    await set_default_commands(bot)

    if settings.USE_WEBHOOK:
        webhook_url = (
            settings.WEBHOOK_URL + settings.WEBHOOK_PATH
            if settings.WEBHOOK_URL
            else f"http://localhost:{settings.WEBHOOK_PORT}{settings.WEBHOOK_PATH}"
        )
        await bot.set_webhook(
            webhook_url,
            drop_pending_updates=settings.drop_pending_updates,
            allowed_updates=dp.resolve_used_update_types(),
        )
    # else:
    # await bot.delete_webhook(drop_pending_updates=settings.drop_pending_updates)

    bot_info = await bot.get_me()

    logger.info(f"Name     - {bot_info.full_name}")
    logger.info(f"Username - @{bot_info.username}")
    logger.info(f"ID       - {bot_info.id}")

    states: dict[bool | None, str] = {
        True: "Enabled",
        False: "Disabled",
        None: "Unknown (This's not a bot)",
    }

    logger.info(f"Groups Mode  - {states[bot_info.can_join_groups]}")
    logger.info(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logger.info(f"Inline Mode  - {states[bot_info.supports_inline_queries]}")

    logger.info("bot started")


async def shutdown() -> None:
    """Need to close Redis and PostgreSQL connection when shutdown."""
    logger.info("bot stopping...")

    await remove_default_commands(bot)

    # await db.close_database()
    await dp.storage.close()

    await dp.fsm.storage.close()
    await bot.session.close()
    # await close_orm()

    logger.info("bot stopped")


async def main() -> None:
    if settings.SENTRY_DSN:
        sentry_loguru = LoguruIntegration(
            level=LoggingLevels.INFO.value,
            event_level=LoggingLevels.INFO.value,
        )
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            enable_tracing=True,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
            integrations=[sentry_loguru],
        )
    logger.add(
        "logs/bot_debug.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="100 KB",
        compression="zip",
    )

    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    if settings.USE_WEBHOOK:
        pass
    else:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
