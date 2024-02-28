from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.utils.i18n.core import I18n
from aiohttp import web
from redis.asyncio import ConnectionPool, Redis

from bot.core.config import I18N_DOMAIN, LOCALES_DIR, settings

app = web.Application()

token = settings.BOT_TOKEN

bot = Bot(token=token, parse_mode=ParseMode.HTML)

redis_client = Redis(
    connection_pool=ConnectionPool(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASS,
        db=0,
    ),
)

storage = RedisStorage(
    redis=redis_client,
    key_builder=DefaultKeyBuilder(with_bot_id=True),
)

dp = Dispatcher(storage=storage)

i18n: I18n = I18n(path=LOCALES_DIR, default_locale="en", domain=I18N_DOMAIN)

DEBUG = settings.DEBUG
