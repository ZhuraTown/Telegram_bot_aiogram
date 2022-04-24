from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types


class StatesAdminUser(StatesGroup):
    start_admin_panel = State()
    get_table = State()
    add_user = State()
    get_info_users = State()

    write_user_name = State()
    write_user_comment = State()
    save_user = State()


class Companies(StatesGroup):
    list_companies = State()


