from aiogram import F, Router, types
from aiogram.filters import Command

from bot_config import database
from pprint import pprint

shop_router = Router()

@shop_router.message(Command("dishes"))
async def show_all_dishes(message: types.Message):
    all_dishes = database.fetch(
        query="SELECT * FROM dishes"
    )
    pprint(all_dishes)
    await message.answer("блюдо из нашего каталога:")
    for dish in all_dishes:
        await message.answer(f"Название: {dish['name']}\nЦена: {dish['price']}")