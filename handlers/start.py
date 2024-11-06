from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    # Кнопки для внешних ссылок
    buttons = [
        [InlineKeyboardButton(text="Наш сайт", url="https://example.com")],
        [InlineKeyboardButton(text="Instagram", url="https://instagram.com")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        "Добро пожаловать в наш ресторан! Здесь вы можете узнать меню, сделать заказ или получить рекомендации.",
        reply_markup=keyboard
    )