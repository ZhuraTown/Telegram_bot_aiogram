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


class StatesUsers(StatesGroup):
    start_user_pamel = State()

    create_new_form = State()

    write_name_work = State()
    select_name_work = State()

    step_stage_work = State()
    write_stage_work = State()

    build_work = State()
    write_build_work = State()
    select_build_work = State()

    write_level_build_work = State()

    step_workers = State()
    write_plan_workers = State()
    write_actually_workers = State()
    finish_write_workers = State()


