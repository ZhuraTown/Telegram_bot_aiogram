from create_bot import bot, dp
from aiogram import executor
from handlers.users import register_handlers_users
from handlers.admin import register_handlers_admin
from handlers.start_work import register_handlers_start_work


async def on_startup(_):
    print('Бот запущен')


async def shutdown(dp):
    await bot.close()


register_handlers_start_work(dp)
register_handlers_users(dp)
register_handlers_admin(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=shutdown)
