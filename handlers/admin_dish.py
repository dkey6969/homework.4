from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot_config import database

admin_dishes_router = Router()
admin_dishes_router.message.filter(
    F.from_user.id == 316777745
)

class Dish(StatesGroup):
    name = State()
    author = State()
    price = State()


@admin_dishes_router.message(Command("newdishes"))
async def create_new_dish(message: types.Message, state: FSMContext):
    print(f"User ID: {message.from_user.id}")
    await state.set_state(Dish.name)
    await message.answer("Задайте название блюда:")

@admin_dishes_router.message(Dish.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Dish.author)
    await message.answer("Задайте автора блюда:")

@admin_dishes_router.message(Dish.author)
async def process_author(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(Dish.price)
    await message.answer("Задайте цену блюда:")

@admin_dishes_router.message(Dish.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)

    data = await state.get_data()
    database.execute(
        query="""
            INSERT INTO dishes(name, author, price)
            VALUES (?, ?, ?)
        """,
        params=(
            data["name"],
            data["author"],
            data["price"]
        )
    )
    await message.answer("Блюдо добавлено")