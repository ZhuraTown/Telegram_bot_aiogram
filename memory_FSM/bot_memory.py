from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


class StatesAdminUser(StatesGroup):
    start_admin_panel = State()

    get_table = State()
    add_user = State()

    get_info_users = State()
    del_user = State()

    builds = State()
    build = State()

    write_build = State()

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
    create_form_sel_name_work = State()
    get_url_form = State()

    get_forms = State()  # Просмотреть формы
    get_form_with_name = State()
    edit_form = State()

    write_name_work = State()  # Добавить наименование работ
    select_name_work = State()  # Выбрать наименование работ

    # Добавление Подрядчика
    edit_user = State()

    edit_user_name = State()
    edit_user_name_correct = State()

    edit_user_pin = State()
    edit_user_pin_correct = State()

    write_user_name = State()
    user_name_correct = State()

    get_info_users = State()
    del_user = State()

    # Здания
    builds = State()
    build = State()

    write_build = State()