from create_bot import dp, create_bot_factory

from handlers.users import register_handlers_users
from handlers.admin import register_handlers_admin
from handlers.start_work import register_handlers_start_work, register_callback_work


register_handlers_start_work(dp)
register_handlers_users(dp)
register_handlers_admin(dp)
register_callback_work(dp)

if __name__ == '__main__':
    create_bot_factory()
