from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .callback_datas import workers_callback, menu_callback, add_users, none_callback, names_work, menu_callback_user, \
    btn_names_msg, workers


class KBLines:

    @staticmethod
    def get_start_panel_btn():
        btn_create_form = InlineKeyboardButton(text='Создать форму', callback_data=menu_callback_user.new(
            step_menu='Step_MAIN', name_btn='Создать форму'
        ))
        btn_get_forms = InlineKeyboardButton(text='Посмотреть созданные формы', callback_data=menu_callback_user.new(
            step_menu='Step_MAIN', name_btn='Посмотреть формы'
        ))
        btn_exit = InlineKeyboardButton(text='Выйти', callback_data=menu_callback_user.new(
            step_menu='Step_MAIN', name_btn='Выйти'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_create_form).row(btn_get_forms).row(btn_exit)

    @staticmethod
    def step_name_work():
        btn_add_name_work = InlineKeyboardButton(text='Добавить наименование работ', callback_data=menu_callback_user.new(
            step_menu='Step_NAME', name_btn='Добавить имя'
        ))
        btn_get_names_work = InlineKeyboardButton(text='Выбрать наименование работ', callback_data=menu_callback_user.new(
            step_menu='Step_NAME', name_btn='Посмотреть'
        ))
        btn_exit = InlineKeyboardButton(text='Главное меню', callback_data=menu_callback_user.new(
            step_menu='Step_NAME', name_btn='Главное'
        ))
        return InlineKeyboardMarkup(row_width=3).row(btn_add_name_work).row(btn_get_names_work).row(btn_exit)

    @staticmethod
    def step_build_work(name_step):
        btn_add_name_work = InlineKeyboardButton(text='Добавить здание', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Добавить здание'
        ))
        btn_get_names_work = InlineKeyboardButton(text='Выбрать здание', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Посмотреть здания'
        ))
        btn_exit = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_add_name_work).row(btn_get_names_work).row(btn_exit)

    @staticmethod
    def save_name(step_name):
        btn_save = InlineKeyboardButton(text='Добавить', callback_data=menu_callback_user.new(
            step_menu=f'{step_name}', name_btn='Добавить'
        ))
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{step_name}', name_btn='Назад'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_save).row(btn_back)

    @staticmethod
    def get_names_one_msg(step_menu: str,
                          names_work_from_db: list):
        kb_inline = InlineKeyboardMarkup(row_width=4)
        for name in names_work_from_db:
            btn_name_work = InlineKeyboardButton(text=f'{name}', callback_data=btn_names_msg.new(
                step_menu=step_menu, name=f'{name}', name_btn='Имя'))
            btn_select = InlineKeyboardButton(text='Выбрать', callback_data=btn_names_msg.new(
                step_menu=step_menu, name=f'{name}', name_btn='Выбрать'
            ))
            btn_del = InlineKeyboardButton(text='Удалить', callback_data=btn_names_msg.new(
                step_menu=step_menu, name=f'{name}', name_btn='Удалить'
            ))
            kb_inline.row(btn_name_work, btn_select, btn_del)
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{step_menu}', name_btn='Назад'
        ))
        kb_inline.row(btn_back)
        return kb_inline

    @staticmethod
    def btn_back(name_step):
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_back)

    @staticmethod
    def btn_next_or_back(name_step):
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'
        ))
        btn_next = InlineKeyboardButton(text='Продолжить', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Продолжить'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_next).row(btn_back)

    @staticmethod
    def get_kb_stage(name_step):
        btn_write_stage = InlineKeyboardButton(text='Ввести этап', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Ввести этап'
        ))
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_write_stage).row(btn_back)

    @staticmethod
    def get_kb_level(name_step):
        btn_write_stage = InlineKeyboardButton(text='Ввести этаж', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Ввести этаж'
        ))
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_write_stage).row(btn_back)

    @staticmethod
    def get_kb_workers(name_step):
        btn_write_stage = InlineKeyboardButton(text='Добавить сотрудника', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Сотрудник'
        ))
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_write_stage).row(btn_back)

    @staticmethod
    def get_workers_menu(name_step):
        # btn_sec = InlineKeyboardButton(text='Охрана', callback_data=workers.new(
        #     step_menu=f'{name_step}', name='Охрана'
        # ))
        # btn_duty = InlineKeyboardButton(text='Дежурный', callback_data=workers.new(
        #     step_menu=f'{name_step}', name='Дежурный'
        # ))
        # btn_worker = InlineKeyboardButton(text='Рабочий', callback_data=workers.new(
        #     step_menu=f'{name_step}', name='Рабочий'
        # ))
        # btn_itr = InlineKeyboardButton(text='ИТР', callback_data=workers.new(
        #     step_menu=f'{name_step}', name='ИТР'
        # ))
        inline_kb = InlineKeyboardMarkup(row_width=3)
        workers_list = ['Охрана', 'Дежурный', 'Рабочий', 'ИТР']
        for worker in workers_list:
            btn_worker = InlineKeyboardButton(text=f'{worker}', callback_data=workers.new(
                step_menu=f'{name_step}', name=f'{worker}', name_btn='Имя'
            ))
            btn_select = InlineKeyboardButton(text='Выбрать', callback_data=workers.new(
                step_menu=f'{name_step}',  name=f'{worker}', name_btn='Выбрать'
            ))
            inline_kb.row(btn_worker, btn_select)
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'
        ))
        inline_kb.row(btn_back)
        return inline_kb

    @staticmethod
    def add_new_worker(name_step):
        btn_write_stage = InlineKeyboardButton(text='Добавить', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Добавить'
        ))
        btn_back = InlineKeyboardButton(text='Продолжить', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Продолжить'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_write_stage).row(btn_back)

###################################################
#     ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ
###################################################
def get_inline_workers_panel():
    btn_sec = InlineKeyboardButton(text='Охрана',
                                   callback_data=workers_callback.new(
                                       type_step='workers',
                                       type_worker='Охрана',
                                       amount=0))
    btn_duty = InlineKeyboardButton(text='Дежурный',
                                    callback_data=workers_callback.new(
                                        type_step='workers',
                                        type_worker='Дежурный',
                                        amount=0))
    btn_worker = InlineKeyboardButton(text='Рабочий',
                                      callback_data=workers_callback.new(
                                          type_step='workers',
                                          type_worker='Рабочий',
                                          amount=0))
    btn_itr = InlineKeyboardButton(text='ИТР',
                                   callback_data=workers_callback.new(
                                       type_step='workers',
                                       type_worker='ИТР',
                                       amount=0))
    btn_skip = InlineKeyboardButton(text='Пропустить',
                                    callback_data=menu_callback.new(
                                        btn_menu='add_users',
                                        type_btn='Пропустить'
                                    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_sec, btn_duty). \
        row(btn_worker, btn_itr).row(btn_skip)


def get_panel_attempt_add_users():
    btn_next = InlineKeyboardButton(text='Продолжить',
                                    callback_data=menu_callback.new(
                                        btn_menu='finish_add',
                                        type_btn='Продолжить'))
    btn_add = InlineKeyboardButton(text='Добавить',
                                   callback_data=menu_callback.new(
                                       btn_menu='finish_add',
                                       type_btn='Добавить'))
    return InlineKeyboardMarkup(row_width=1).row(btn_next).row(btn_add)


def get_btn_add_users():
    btn_empty = InlineKeyboardButton(text=' ', callback_data=none_callback.new(
        none_call='empty'
    ))
    btn_add_1 = InlineKeyboardButton(text='+1', callback_data=add_users.new(
        type='1', type_btn='plus'
    ))
    btn_add_5 = InlineKeyboardButton(text='+5', callback_data=add_users.new(
        type='5', type_btn='plus'
    ))
    btn_add_10 = InlineKeyboardButton(text='+10', callback_data=add_users.new(
        type='10', type_btn='plus'
    ))
    btn_minus_1 = InlineKeyboardButton(text='-1', callback_data=add_users.new(
        type='1', type_btn='minus'
    ))
    btn_minus_5 = InlineKeyboardButton(text='-5', callback_data=add_users.new(
        type='5', type_btn='minus'
    ))
    btn_minus_10 = InlineKeyboardButton(text='-10', callback_data=add_users.new(
        type='10', type_btn='minus'))
    btn_attempt = InlineKeyboardButton(text='Подтвердить', callback_data=add_users.new(
        type='access', type_btn='Подтвердить'
    ))
    btn_cancel = InlineKeyboardButton(text='Отменить', callback_data=add_users.new(
        type='cancel', type_btn='Отменить'
    ))
    return InlineKeyboardMarkup(row_width=4).row(btn_add_1, btn_add_5, btn_add_10). \
        row(btn_empty).row(btn_minus_1, btn_minus_5, btn_minus_10).row(btn_attempt, btn_cancel)


###############################
#       ГЛАВОЕ МЕНЮ НАЧАЛО
###############################
def save_form_or_add_string(step_):
    btn_save_form = InlineKeyboardButton(text='Сохранить форму', callback_data=menu_callback.new(
        btn_menu='save_form', type_btn='Сохранить форму'
    ))
    btn_add_string = InlineKeyboardButton(text='Добавить строку', callback_data=menu_callback.new(
        btn_menu='save_form', type_btn='Добавить строку'
    ))
    btn_delete = InlineKeyboardButton(text='Вернуться в главное Меню', callback_data=menu_callback.new(
        btn_menu='save_form', type_btn='Вернуться'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_save_form).row(btn_add_string).row(btn_delete)


def get_main_menu_user_panel():
    btn_create_form = InlineKeyboardButton(text='Создать форму', callback_data=menu_callback.new(
        btn_menu='main_menu', type_btn='Создать форму'
    ))
    btn_get_forms = InlineKeyboardButton(text='Посмотреть созданные формы', callback_data=menu_callback.new(
        btn_menu='main_menu', type_btn='Посмотреть формы'
    ))
    btn_exit = InlineKeyboardButton(text='Выйти', callback_data=menu_callback.new(
        btn_menu='main_menu', type_btn='Выйти'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_create_form).row(btn_get_forms).row(btn_exit)


##############################################
#       ЭТАП ДОБАВЛЕНИЕ НАИМЕНОВАНИЯ РАБОТЫ
##############################################
def step_select_or_write_name_work():
    btn_add_name_work = InlineKeyboardButton(text='Добавить наименование работ', callback_data=menu_callback.new(
        btn_menu='main_menu', type_btn='Добавить работу'
    ))
    btn_get_names_work = InlineKeyboardButton(text='Выбрать наименование работ', callback_data=menu_callback.new(
        btn_menu='main_menu', type_btn='Посмотреть наименования'
    ))
    btn_exit = InlineKeyboardButton(text='Главное меню', callback_data=menu_callback.new(
        btn_menu='main_menu', type_btn='Главное меню'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_add_name_work).row(btn_get_names_work).row(btn_exit)


def back_to_main_menu_user():
    btn_exit = InlineKeyboardButton(text='Главное меню', callback_data=menu_callback.new(
        btn_menu='main_menu', type_btn='Главное меню'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_exit)


def save_name_work():
    btn_save = InlineKeyboardButton(text='Добавить', callback_data=menu_callback.new(
        btn_menu='name_work', type_btn='Добавить'
    ))
    btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback.new(
        btn_menu='name_work', type_btn='Назад'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_save).row(btn_back)


def btn_back_menu(add_btn_next=True):
    btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback.new(
        btn_menu='name_work', type_btn='Назад'
    ))
    btn_next = InlineKeyboardButton(text='Продолжить', callback_data=menu_callback.new(
        btn_menu='name_work', type_btn='Продолжить'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_next).row(btn_back) if add_btn_next \
        else InlineKeyboardMarkup(row_width=2).row(btn_back)


def btn_back_names_work():
    btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback.new(
        btn_menu='name_stage', type_btn='Назад'
    ))
    btn_next = InlineKeyboardButton(text='Продолжить', callback_data=menu_callback.new(
        btn_menu='name_stage', type_btn='Продолжить'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_next).row(btn_back)


#######################
def get_names_work_one_msg(names_work_from_db):
    kb_inline = InlineKeyboardMarkup(row_width=4)
    for name in names_work_from_db:
        btn_name_work = InlineKeyboardButton(text=f'{name}', callback_data=names_work.new(
            name_work=f'{name}', type_btn='Имя'))
        btn_select = InlineKeyboardButton(text='Выбрать', callback_data=names_work.new(
            name_work=f'{name}', type_btn='Выбрать'
        ))
        btn_del = InlineKeyboardButton(text='Удалить', callback_data=names_work.new(
            name_work=f'{name}', type_btn='Удалить'
        ))
        kb_inline.row(btn_name_work, btn_select, btn_del)
    return kb_inline


#########################################
#   ЭТАП ДОБАВЛЕНИЕ ЭТАПОВ РАБОТЫ
#########################################
def get_kb_stage():
    btn_write_stage = InlineKeyboardButton(text='Ввести этап', callback_data=menu_callback.new(
        btn_menu='name_stage', type_btn='Ввести этап'
    ))
    btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback.new(
        btn_menu='name_stage', type_btn='Назад'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_write_stage).row(btn_back)


##########################################
#        ЭТАП ДОБАВЛЕНИЯ ЗДАНИЯ
##########################################

def step_select_or_write_build_work():
    btn_add_name_work = InlineKeyboardButton(text='Добавить здание', callback_data=menu_callback.new(
        btn_menu='name_build', type_btn='Добавить здание'
    ))
    btn_get_names_work = InlineKeyboardButton(text='Выбрать здание', callback_data=menu_callback.new(
        btn_menu='name_build', type_btn='Посмотреть здания'
    ))
    btn_exit = InlineKeyboardButton(text='Назад', callback_data=menu_callback.new(
        btn_menu='name_build', type_btn='Назад'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_add_name_work).row(btn_get_names_work).row(btn_exit)


def save_name_build():
    btn_save = InlineKeyboardButton(text='Добавить', callback_data=menu_callback.new(
        btn_menu='name_build', type_btn='Добавить'
    ))
    btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback.new(
        btn_menu='name_build', type_btn='Назад'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_save).row(btn_back)


def btn_back_builds_work(add_btn_next=True):
    btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback.new(
        btn_menu='name_stage', type_btn='Назад'
    ))
    btn_next = InlineKeyboardButton(text='Продолжить', callback_data=menu_callback.new(
        btn_menu='name_stage', type_btn='Продолжить'
    ))
    return InlineKeyboardMarkup(row_width=2).row(btn_next).row(btn_back) if add_btn_next \
        else InlineKeyboardMarkup(row_width=2).row(btn_back)
