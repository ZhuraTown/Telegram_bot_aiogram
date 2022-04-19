from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types


class StatesAdmin(StatesGroup):
    admin_panel_start = State()
    admin_table_menu = State()
    admin_add_user = State()
    admin_get_users = State()
    admin_back_panel = State()


class StatesUser(StatesGroup):
    user_panel_start = State()
    user_create_form = State()
    user_edit_form = State()
    form_name_work = State()


class RegisterUser(StatesGroup):
    write_name = State()
    write_comment = State()
    add_or_delete = State()
