from aiogram import Router, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

opros_router = Router()

class RestaurantReview(StatesGroup):
    name = State()
    phone_or_instagram = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

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
    await state.update_data(visit_date=message.text)
    await state.set_state(RestaurantReview.food_rating)
    await message.answer("Оцените качество блюд")

@opros_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    await state.set_state(RestaurantReview.cleanliness_rating)
    await message.answer("Оцените чистоту заведения")

@opros_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    await state.update_data(cleanliness_rating=message.text)
    await state.set_state(RestaurantReview.extra_comments)
    await message.answer("Можете добавить свой отзыв ресторану")

@opros_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    await message.answer("Спасибо за ваш отзыв!")
    data = await state.get_data()
    print(data)
    await state.clear()