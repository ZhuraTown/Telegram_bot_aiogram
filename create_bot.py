import asyncio

from decouple import config
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data_base.db_commands import CommandsDB
from reminder.reminder_table import remind_fill_out_form

API_TOKEN = config('API_TOKEN')

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Бот запущен')
    CommandsDB.create_db()
    asyncio.create_task(remind_fill_out_form(bot=bot))


async def shutdown(dp):
    await bot.close()


def create_bot_factory() -> None:
    """ Инициализация бота, добавление задач, запуск бота"""
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=shutdown)



