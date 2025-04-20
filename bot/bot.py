import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram import filters
from config import API_TOKEN
from handlers import cmd_start, cmd_search

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

dp.message.register(cmd_start, filters.Command("start"))
dp.message.register(cmd_search, filters.Command("search"))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
