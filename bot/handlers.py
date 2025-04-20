from aiogram import types
from services import get_books

async def cmd_start(message: types.Message):
    await message.answer("Здравствуйте! Введите /search <название книги>, чтобы найти книгу в библиотеках Санкт-Петербурга.")

async def cmd_search(message: types.Message):
    query = message.text.split(maxsplit=1)
    if len(query) < 2:
        await message.reply("Пожалуйста, укажите название книги после команды /search.")
        return
    await message.reply("Ищу книги, пожалуйста подождите...")
    books = await get_books(query[1])
    await message.reply(books)


