from aiogram import Router, types
from aiogram.filters import Command

minfo_router = Router()

@minfo_router.message(Command('minfo'))
async def minfo_handler(message: types.Message):
    name = message.from_user.first_name
    user_id = message.from_user.id
    msg = f'ваш айди {name},{user_id}'
    await message.answer(msg)
