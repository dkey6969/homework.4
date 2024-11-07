from aiogram import Router, types
from aiogram.filters import Command
from random import choice
from aiogram.types import FSInputFile

random_recipe_router = Router()

recipes = [
    {"name": "Пицца", "photo": "images/recipe1.jpg",
     "description": "Рецепт: Тонкое тесто, томатный соус, сыр и свежие овощи."},
    {"name": "Паста", "photo": "images/recipe2a.jpg", "description": "Рецепт: Спагетти с соусом песто и пармезаном."},
]


@random_recipe_router.message(Command("random"))
async def random_recipe_handler(message: types.Message):
    recipe = choice(recipes)
    photo = FSInputFile(recipe['photo'])
    await message.answer_photo(
        photo=photo,
        caption=f"{recipe['name']}\n{recipe['description']}"
    )
