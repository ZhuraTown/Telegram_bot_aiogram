from create_bot import Bot, dp
from aiogram import executor
from handlers.users import register_handlers_users


async def on_startup(_):
    print('Бот запущен')

register_handlers_users(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

