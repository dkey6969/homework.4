from aiogram import Router, types
from aiogram.filters import Command
from bot_config import database

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    user_id = message.from_user.id
    user_count = len(database.fetch("SELECT DISTINCT telegram_id FROM users"))

    if not database.fetch("SELECT * FROM users WHERE telegram_id = ?", (user_id,)):
        database.execute("INSERT INTO users (telegram_id) VALUES (?)", (user_id,))

    msg = f"Привет, {name}! Наш бот обслуживает уже {user_count} пользователей."

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Наш инстаграм",
                    url="https://instagram.com/geeks"
                ),
                types.InlineKeyboardButton(
                    text="Наш сайт",
                    url="https://geeks.kg"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="О Нас",
                    callback_data="about"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Оцените ресторан",
                    callback_data="review"
                )
            ]
        ]
    )
    await message.answer(msg, reply_markup=kb)