from aiogram import types
from bot.loader import bot
from bot.loader import db
from bot.loader import dp


@dp.message_handler(commands="start")
async def start_message(message: types.Message):
    """welcome message."""
    if await db.verification(message.from_user.id):
        await bot.send_message(message.chat.id, "👋 Hello, I remember you.")
    else:
        if message.from_user.first_name != "None":
            name = message.from_user.first_name
        elif message.from_user.username != "None":
            name = message.from_user.username
        elif message.from_user.last_name != "None":
            name = message.from_user.last_name
        else:
            name = ""
        await db.add_user(message.from_user.id, name, message.from_user.locale.language_name)
        await bot.send_message(message.chat.id, "ℹ️ <b>[About]\n</b> Bot is a template for future projects.")


@dp.message_handler(commands=("help", "info", "about"))
async def give_info(message: types.Message):
    """the target of this bot."""
    await bot.send_message(message.chat.id, "ℹ️ <b>[About]\n</b> Bot is a template for future projects.")


@dp.message_handler(commands="contacts")
async def give_contacts(message: types.Message):
    """ссылка на код проекта."""
    btn_link = types.InlineKeyboardButton(
        text="Go to GitHub.", url="https://github.com/DONSIMON92/telegram-bot-template"
    )
    keyboard_link = types.InlineKeyboardMarkup().add(btn_link)
    await bot.send_message(
        message.chat.id,
        "👨‍💻 the project code is available on Github.",
        reply_markup=keyboard_link,
    )


@dp.message_handler(commands="settings")
async def give_settings(message: types.Message):
    """справка по настройкам."""
    name = await db.get_name(message.from_user.id)
    lang = await db.get_lang(message.from_user.id)
    btn_name = types.InlineKeyboardButton(text=f"name: {name}", callback_data="name")
    btn_lang = types.InlineKeyboardButton(text=f"language: {lang}", callback_data="lang")
    keyboard_settings = types.InlineKeyboardMarkup().add(btn_name, btn_lang)
    await bot.send_message(message.chat.id, "⚙️ eSettings", reply_markup=keyboard_settings)


@dp.callback_query_handler(lambda c: c.data == "name")
async def alter_name(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.id, "How should I address you?")
    await bot.answer_callback_query(callback_query.id)


@dp.callback_query_handler(lambda c: c.data == "lang")
async def alter_lang(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.id, "Choose language:")
    await bot.answer_callback_query(callback_query.id, "Choose language:")


@dp.message_handler(content_types="text")
async def text_handler(message: types.Message):
    await bot.send_message(message.chat.id, "Text processing can take place here.")


@dp.message_handler()
async def unknown_message(message: types.Message):
    if not message.is_command():
        await bot.send_message(message.chat.id, "❌ I don't know how to work with this format.")
    else:
        await message.answer("❌ Invalid command.")
