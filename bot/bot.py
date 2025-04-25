import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram import filters
from config import API_TOKEN
from handlers import cmd_start, cmd_search

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.message.register(cmd_start, filters.Command("start"))
dp.message.register(cmd_search, filters.Command("search"))

async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='search', description='Поиск книги по ее названию')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

async def start_bot():
    await set_commands()
    logging.info("Бот успешно запущен!")

async def stop_bot():
    await bot.session.close()
    logging.info("Бот успешно остановлен!")

async def main():
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
