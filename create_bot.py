from apscheduler.schedulers.asyncio import AsyncIOScheduler
from decouple import config
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data_base.db_commands import CommandsDB
from reminder.reminder_table import remind_fill_out_form, del_remind_fill_out_form

API_TOKEN = config('API_TOKEN')

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
schedule = AsyncIOScheduler(timezone='Europe/Moscow')

msg = 'Табель времени еще не заполнен.'


async def on_startup(_):
    print('Бот запущен')
    CommandsDB.create_db()
    schedule.start()
    schedule.add_job(remind_fill_out_form, trigger='cron', day_of_week='mon-fri', hour=9, minute=15, args=[bot, msg])
    schedule.add_job(del_remind_fill_out_form, trigger='cron', day_of_week='mon-fri', hour=23, minute=20)


async def shutdown(dp):
    schedule.shutdown()
    await bot.close()


def create_bot_factory() -> None:
    """ Инициализация бота, добавление задач, запуск бота"""
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=shutdown)



