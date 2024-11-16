from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime
from bot_config import database

review_router = Router()

class Review(StatesGroup):
    name = State()
    phone_or_instagram = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@review_router.message(Command("stop"))
@review_router.message(F.text == "стоп")
async def stop_review(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Отзыв прерван")

@review_router.callback_query(F.data == "review")
async def start_review(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Review.name)
    await callback_query.message.answer("Как вас зовут?")

@review_router.message(Review.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Review.phone_or_instagram)
    await message.answer("Напишите свой Instagram или номер телефона")

@review_router.message(Review.phone_or_instagram)
async def process_phone_or_instagram(message: types.Message, state: FSMContext):
    await state.update_data(phone_or_instagram=message.text)
    await state.set_state(Review.visit_date)
    await message.answer("Когда вы посещали наше заведение? (формат: дд.мм.гггг)")

@review_router.message(Review.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    try:
        visit_date = datetime.strptime(message.text, "%d.%m.%Y")
        await state.update_data(visit_date=visit_date.strftime("%d.%m.%Y"))
        await state.set_state(Review.food_rating)
        await message.answer("Оцените качество блюд (от 1 до 5)")
    except ValueError:
        await message.answer("Введите дату в формате дд.мм.гггг")

@review_router.message(Review.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(food_rating=int(message.text))
        await state.set_state(Review.cleanliness_rating)
        await message.answer("Оцените чистоту заведения (от 1 до 5)")
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5")

@review_router.message(Review.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(cleanliness_rating=int(message.text))
        await state.set_state(Review.extra_comments)
        await message.answer("Добавьте дополнительный отзыв, если хотите")
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5")

@review_router.message(Review.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    data = await state.get_data()

    database.create_tables()

    database.execute(
        query="""
        INSERT INTO reviews (
            name, phone_or_instagram, visit_date, 
            food_rating, cleanliness_rating, extra_comments
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        params=(
            data["name"],
            data["phone_or_instagram"],
            data["visit_date"],
            data["food_rating"],
            data["cleanliness_rating"],
            data["extra_comments"],
        ),
    )

    await message.answer("Спасибо за ваш отзыв!")
    await state.clear()