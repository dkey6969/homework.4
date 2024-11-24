from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot_config import database

admin_dishes_router = Router()
admin_dishes_router.message.filter(
    F.from_user.id == 7228978162
)

class Dish(StatesGroup):
    name = State()
    description = State()
    price = State()
    category = State()

@admin_dishes_router.message(Command("newdishes"))
async def create_new_dish(message: types.Message, state: FSMContext):
    await state.set_state(Dish.name)
    await message.answer("Задайте название блюда:")

@admin_dishes_router.message(Dish.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Dish.description)
    await message.answer("Задайте описание блюда:")

@admin_dishes_router.message(Dish.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Dish.price)
    await message.answer("Задайте цену блюда:")

@admin_dishes_router.message(Dish.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    categories = database.fetch("SELECT id, name FROM dish_categories")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        keyboard.add(category["name"])
    await state.set_state(Dish.category)
    await message.answer("Выберите категорию блюда:", reply_markup=keyboard)

@admin_dishes_router.message(Dish.category)
async def process_category(message: types.Message, state: FSMContext):
    category_name = message.text
    category = database.fetch("SELECT id FROM dish_categories WHERE name = ?", (category_name,))
    if category:
        category_id = category[0]["id"]
        data = await state.get_data()
        database.execute(
            query="""
                INSERT INTO dishes(name, description, price, category_id)
                VALUES (?, ?, ?, ?)
            """,
            params=(
                data["name"],
                data["description"],
                data["price"],
                category_id
            )
        )
        await message.answer("Блюдо добавлено")
    else:
        await message.answer("Категория не найдена. Пожалуйста, выберите из предложенных.")
    await state.clear()