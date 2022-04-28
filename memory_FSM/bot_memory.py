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
    start_user_pamel = State()  # Начало работы, главное меню

    create_new_form = State()  # Создать форму
    get_forms = State()  # Просмотреть форму

    step_name_work = State()  # Шаг Наименования работ
    write_name_work = State()  # Добавить наименование работ
    select_name_work = State()  # Выбрать наименование работ

    step_stage_work = State()  # Этап
    write_stage_work = State()  # Ввести этап работы

    step_build_work = State()  # Здания
    write_build_work = State()  # Ввести наименование здания
    select_build_work = State()  # Выбрать наименование здания

    step_level_build_work = State()  # Этаж
    write_level_build_work = State()  # Ввести этаж

    step_workers = State()  # Сотрудники
    select_plan_workers = State()
    write_plan_workers = State()
    write_actually_workers = State()
    finish_write_workers = State()
