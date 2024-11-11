from aiogram import Router, types, F
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    msg = f"Привет, {name}"
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
                    text="оцените ресторан",
                    callback_data="riewe"
                )
            ]
        ]
    )
    await message.answer(msg, reply_markup=kb)

@start_router.callback_query(F.data == "riewe")
async def start_review_dialog(callback: types.CallbackQuery, state):
    await state.set_state("RestaurantReview:name")
    await callback.message.answer("Как вас зовут?")