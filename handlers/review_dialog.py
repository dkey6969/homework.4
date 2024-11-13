from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime

opros_router = Router()

class RestaurantReview(StatesGroup):
    name = State()
    phone_or_instagram = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@opros_router.callback_query(F.data == "review")
async def start_review_dialog(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RestaurantReview.name)
    await callback.message.answer("Как вас зовут?")

@opros_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.phone_or_instagram)
    await message.answer("Напишите свой Instagram или номер телефона")

@opros_router.message(RestaurantReview.phone_or_instagram)
async def process_phone_or_instagram(message: types.Message, state: FSMContext):
    await state.update_data(phone_or_instagram=message.text)
    await state.set_state(RestaurantReview.visit_date)
    await message.answer("Когда последний раз вы были в нашем заведении?")

@opros_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    try:
        visit_date = datetime.strptime(message.text, "%d.%m.%Y")
        await state.update_data(visit_date=visit_date.strftime("%d.%m.%Y"))
        await state.set_state(RestaurantReview.food_rating)
        await message.answer("Оцените качество блюд (от 1 до 5)")
    except ValueError:
        await message.answer("Пожалуйста, введите дату в формате")

@opros_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(food_rating=int(message.text))
        await state.set_state(RestaurantReview.cleanliness_rating)
        await message.answer("Оцените чистоту заведения (от 1 до 5)")
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5 для оценки качества блюд")

@opros_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        await state.update_data(cleanliness_rating=int(message.text))
        await state.set_state(RestaurantReview.extra_comments)
        await message.answer("Можете добавить свой отзыв ресторану")
    else:
        await message.answer("Пожалуйста, введите число от 1 до 5 для оценки чистоты")

@opros_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    await message.answer("Спасибо за ваш отзыв!")
    data = await state.get_data()
    print(data)
    await state.clear()