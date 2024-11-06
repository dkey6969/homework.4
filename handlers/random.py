from aiogram import Router, types
from aiogram.filters import Command
from random import choice
from aiogram.types import FSInputFile

random_recipe_router = Router()

recipes = [
    {"name": "Пицца", "photo": "images/pizza.jpg", "recipe1": "Рецепт: Тонкое тесто, томатный соус, сыр и свежие овощи."},
    {"name": "Паста", "photo": "images/pasta.jpg", "recipe2": "Рецепт: Спагетти с соусом песто и пармезаном."},
]

@random_recipe_router.message(Command("random_recipe"))
async def random_recipe_handler(message: types.Message):
    recipe = choice(recipes)
    photo = FSInputFile(recipe['photo'])
    await message.answer_photo(photo, caption=recipe["caption"])