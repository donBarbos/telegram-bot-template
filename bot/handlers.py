from aiogram import types
from bot.loader import bot, db, dp
from bot.texts import button_texts, message_texts


@dp.message_handler(commands="start")
async def start_message(message: types.Message) -> None:
    """welcome message."""
    if await db.verification(message.from_user.id):
        await bot.send_message(message.chat.id, message_texts["welcome"])
        return
    first_name = message.from_user.first_name
    username = message.from_user.username
    last_name = message.from_user.last_name
    name = first_name or username or last_name or ""
    await db.add_user(message.from_user.id, name, message.from_user.locale.language_name)
    await bot.send_message(message.chat.id, message_texts["about"])


@dp.message_handler(commands=("help", "info", "about"))
async def give_info(message: types.Message) -> None:
    """the target of this bot."""
    await bot.send_message(message.chat.id, message_texts["about"])


@dp.message_handler(commands="contacts")
async def give_contacts(message: types.Message) -> None:
    """ссылка на код проекта."""
    btn_link = types.InlineKeyboardButton(
        text=button_texts["github"], url="https://github.com/donBarbos/telegram-bot-template"
    )
    keyboard_link = types.InlineKeyboardMarkup().add(btn_link)
    await bot.send_message(
        message.chat.id,
        message_texts["github"],
        reply_markup=keyboard_link,
    )


@dp.message_handler(commands="settings")
async def give_settings(message: types.Message) -> None:
    """справка по настройкам."""
    name = await db.get_name(message.from_user.id)
    lang = await db.get_lang(message.from_user.id)
    btn_name = types.InlineKeyboardButton(text=f"name: {name}", callback_data="name")
    btn_lang = types.InlineKeyboardButton(text=f"language: {lang}", callback_data="lang")
    keyboard_settings = types.InlineKeyboardMarkup().add(btn_name, btn_lang)
    await bot.send_message(message.chat.id, message_texts["settings"], reply_markup=keyboard_settings)


@dp.callback_query_handler(lambda c: c.data == "name")
async def alter_name(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.id, message_texts["address"])
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == "lang")
async def alter_lang(callback_query: types.CallbackQuery) -> None:
    await bot.send_message(callback_query.id, message_texts["language"])
    await bot.answer_callback_query(callback_query.id, message_texts["language"])


@dp.message_handler(content_types="text")
async def text_handler(message: types.Message) -> None:
    await bot.send_message(message.chat.id, message_texts["text"])


@dp.message_handler()
async def unknown_message(message: types.Message) -> None:
    if not message.is_command():
        await bot.send_message(message.chat.id, message_texts["format_error"])
    else:
        await message.answer(message_texts["command_error"])
