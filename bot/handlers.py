from aiogram import types
from services import get_books
import logging

async def cmd_start(message: types.Message):
    logging.debug(message.text)
    logging.info("Вызов стартовой функции cmd_start")
    await message.answer("Здравствуйте! Введите /search <название книги>, чтобы найти книгу в библиотеках Санкт-Петербурга.")

async def cmd_search(message: types.Message):
    logging.info("Вызов функции cmd_search")
    query = message.text.split(maxsplit=1)
    if len(query) < 2:
        logging.warning("Ошибка в использывании команды cmd_search")
        await message.reply("Пожалуйста, укажите название книги после команды /search.")
        return
    await message.reply("Ищу книги, пожалуйста подождите...")
    books = await get_books(query[1])
    await message.reply(books)


