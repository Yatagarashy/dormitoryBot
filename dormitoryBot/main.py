import asyncio
import logging
import sqlite3
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Bot, Dispatcher

from handlers import registration
from handlers import entering_information

from middlewares.session_middleware import DbSessionMiddleware

from settings import TOKEN





logging.basicConfig(level=logging.INFO)


async def main():

    storage = RedisStorage.from_url('redis://localhost:6379/0')

    bot = Bot(token=TOKEN, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()


    dp.update.outer_middleware(DbSessionMiddleware(cursor=cursor, connection=connection))

    dp.include_router(entering_information.router)
    dp.include_router(registration.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())