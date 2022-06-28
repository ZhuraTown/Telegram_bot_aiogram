from create_bot import bot, dp
from aiogram import executor

from data_base.db_commands import CommandsDB
from handlers.users import register_handlers_users
from handlers.admin import register_handlers_admin
from handlers.start_work import register_handlers_start_work, register_callback_work

from reminder.reminder_table import remind_fill_out_form

async def on_startup(_):
    print('Бот запущен')
    CommandsDB.create_db()


async def shutdown(dp):
    await bot.close()



register_handlers_start_work(dp)
register_handlers_users(dp)
register_handlers_admin(dp)
register_callback_work(dp)

if __name__ == '__main__':
    # dp.loop.create_task(remind_fill_out_form(1))
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=shutdown)
