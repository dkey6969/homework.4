from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

review_router = Router()

class RestaurantReview(StatesGroup):
    name = State()
    phone_or_instagram = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@review_router.message(Command("review"))
async def start_review(message: types.Message, state: FSMContext):
    await state.set_state(RestaurantReview.name)
    await message.answer("Как вас зовут?")

@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.phone_or_instagram)
    await message.answer("Ваш номер телефона или Instagram?")

@review_router.message(RestaurantReview.phone_or_instagram)
async def process_phone_or_instagram(message: types.Message, state: FSMContext):
    await state.update_data(phone_or_instagram=message.text)
    await state.set_state(RestaurantReview.visit_date)
    await message.answer("Дата вашего посещения заведения?")

@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    food_rating_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Плохо")],
            [types.KeyboardButton(text="Удовлетворительно")],
            [types.KeyboardButton(text="Хорошо")],
            [types.KeyboardButton(text="Отлично")]
        ],
        resize_keyboard=True
    )
    await message.answer("Как оцениваете качество еды?", reply_markup=food_rating_keyboard)
    await state.set_state(RestaurantReview.food_rating)

@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    if message.text not in ["Плохо", "Удовлетворительно", "Хорошо", "Отлично"]:
        await message.answer("Пожалуйста, выберите один из вариантов: 'Плохо', 'Удовлетворительно', 'Хорошо' или 'Отлично'.")
        return

    await state.update_data(food_rating=message.text)
    cleanliness_rating_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Плохо")],
            [types.KeyboardButton(text="Удовлетворительно")],
            [types.KeyboardButton(text="Хорошо")],
            [types.KeyboardButton(text="Отлично")]
        ],
        resize_keyboard=True
    )
    await message.answer("Как оцениваете чистоту заведения?", reply_markup=cleanliness_rating_keyboard)
    await state.set_state(RestaurantReview.cleanliness_rating)