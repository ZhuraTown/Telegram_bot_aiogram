from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


class StatesAdminUser(StatesGroup):
    start_admin_panel = State()

    get_table = State()
    add_user = State()

    get_info_users = State()
    del_user = State()

    edit_user = State()

    edit_user_name = State()
    edit_user_name_correct = State()

    edit_user_pin = State()
    edit_user_pin_correct = State()

    write_user_name = State()
    user_name_correct = State()

class AuthorizationUser(StatesGroup):
    write_password = State()
    correct_password_user = State()
    correct_password_admin = State()


class StatesUsers(StatesGroup):
    start_user_panel = State()  # Начало работы, главное меню

    create_new_form = State()  # Создать форму

    get_forms = State()  # Просмотреть формы
    get_form_with_name = State()
    edit_form_with_name = State()

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
    select_plan_workers = State()  # Выбор типа сотрудника
    write_plan_workers = State()  # Ввести количество сотрудников ПЛАН
    write_actually_workers = State()  # Ввести количество сотрудников ФАКТ
    finish_write_workers = State()  # Добавить сотрудников/ Продолжить

    step_save_or_add_string = State()  # Создание/добавление(строки) формы
    save_form = State()  # Сохранить форму
    add_string = State()  #  Добавить строку


