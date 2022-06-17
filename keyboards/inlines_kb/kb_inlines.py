from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .callback_datas import menu_callback_user, btn_names_msg, workers


class KBLines:

    @staticmethod
    def get_start_panel_btn():
        btn_create_form = InlineKeyboardButton(text='Создать форму', callback_data=menu_callback_user.new(
            step_menu='Step_MAIN', name_btn='Создать форму'
        ))
        btn_get_forms = InlineKeyboardButton(text='Посмотреть созданные формы', callback_data=menu_callback_user.new(
            step_menu='Step_MAIN', name_btn='Посмотреть'
        ))
        btn_exit = InlineKeyboardButton(text='Выйти', callback_data=menu_callback_user.new(
            step_menu='Step_MAIN', name_btn='Выйти'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_create_form).row(btn_get_forms).row(btn_exit)

    # @staticmethod
    # def step_name_work():
    #     btn_add_name_work = InlineKeyboardButton(text='Добавить наименование работ',
    #                                              callback_data=menu_callback_user.new(
    #                                                  step_menu='Step_NAME', name_btn='Добавить имя'
    #                                              ))
    #     btn_get_names_work = InlineKeyboardButton(text='Выбрать наименование работ',
    #                                               callback_data=menu_callback_user.new(
    #                                                   step_menu='Step_NAME', name_btn='Посмотреть'
    #                                               ))
    #     btn_exit = InlineKeyboardButton(text='Главное меню', callback_data=menu_callback_user.new(
    #         step_menu='Step_NAME', name_btn='Главное'
    #     ))
    #     return InlineKeyboardMarkup(row_width=3).row(btn_add_name_work).row(btn_get_names_work).row(btn_exit)

    # @staticmethod
    # def step_build_work(name_step):
    #     btn_add_name_work = InlineKeyboardButton(text='Добавить здание', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Добавить здание'
    #     ))
    #     btn_get_names_work = InlineKeyboardButton(text='Выбрать здание', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Посмотреть здания'
    #     ))
    #     btn_exit = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Назад'
    #     ))
    #     return InlineKeyboardMarkup(row_width=2).row(btn_add_name_work).row(btn_get_names_work).row(btn_exit)

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
    def get_names_work_forms(step_menu: str, data_works: list):
        kb_inline = InlineKeyboardMarkup(row_width=2)
        for data in data_works:
            btn_name_work = InlineKeyboardButton(text=f'{data[0]}', callback_data=btn_names_msg.new(
                step_menu=step_menu, name=f'{data[1]},{data[3]}', name_btn='Форма'))
            btn_contractor = InlineKeyboardButton(text=f'{data[2]}', callback_data=btn_names_msg.new(
                step_menu=step_menu, name=f'{data[1]},{data[3]}', name_btn='Форма'))
            kb_inline.row(btn_name_work, btn_contractor)
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{step_menu}', name_btn='Назад'
        ))
        kb_inline.row(btn_back)
        return kb_inline

    # @staticmethod
    # def panel_name_work(name_step):
    #     btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Назад'
    #     ))
    #     btn_edit = InlineKeyboardButton(text='Изменить', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Изменить'
    #     ))
    #     btn_del = InlineKeyboardButton(text='Удалить', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Удалить'
    #     ))
    #     # return InlineKeyboardMarkup(row_width=1).row(btn_edit, btn_del).row(btn_back)
    #     return InlineKeyboardMarkup(row_width=1).row(btn_back)

    # @staticmethod
    # def get_names_one_msg(step_menu: str,
    #                       names_work_from_db: list):
    #     kb_inline = InlineKeyboardMarkup(row_width=4)
    #     for name in names_work_from_db:
    #         btn_name_work = InlineKeyboardButton(text=f'{name[1]}', callback_data=btn_names_msg.new(
    #             step_menu=step_menu, name=f'{name[0]}', name_btn='select'))
    #         kb_inline.row(btn_name_work)
    #     btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
    #         step_menu=f'{step_menu}', name_btn='Назад'
    #     ))
    #     kb_inline.row(btn_back)
    #     return kb_inline

    # @staticmethod
    # def get_names_work_one_msg(step_menu: str,
    #                            names_work_from_db: list):
    #     kb_inline = InlineKeyboardMarkup(row_width=4)
    #     for name in names_work_from_db:
    #         btn_name_work = InlineKeyboardButton(text=f'{name[1]}', callback_data=btn_names_msg.new(
    #             step_menu=step_menu, name=f'{name[0]}', name_btn='select'))
    #         kb_inline.row(btn_name_work,)
    #     btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
    #         step_menu=f'{step_menu}', name_btn='Назад'
    #     ))
    #     kb_inline.row(btn_back)
    #     return kb_inline

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
    def btn_del_or_back(name_step):
        btn_back = InlineKeyboardButton(text='Удалить', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Удалить'
        ))
        btn_next = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_next, btn_back)

    # @staticmethod
    # def get_kb_stage(name_step):
    #     btn_write_stage = InlineKeyboardButton(text='Ввести этап', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Ввести этап'
    #     ))
    #     btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Назад'
    #     ))
    #     return InlineKeyboardMarkup(row_width=2).row(btn_write_stage).row(btn_back)

    # @staticmethod
    # def get_kb_level(name_step):
    #     btn_write_stage = InlineKeyboardButton(text='Ввести этаж', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Ввести этаж'
    #     ))
    #     btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Назад'
    #     ))
    #     return InlineKeyboardMarkup(row_width=2).row(btn_write_stage).row(btn_back)

    # @staticmethod
    # def get_kb_workers(name_step):
    #     btn_write_stage = InlineKeyboardButton(text='Добавить сотрудника', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Сотрудник'
    #     ))
    #     btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Назад'
    #     ))
    #     return InlineKeyboardMarkup(row_width=2).row(btn_write_stage).row(btn_back)

    # @staticmethod
    # def get_workers_menu(name_step):
    #     inline_kb = InlineKeyboardMarkup(row_width=3)
    #     workers_list = ['Охрана', 'Дежурный', 'Рабочий', 'ИТР']
    #     for worker in workers_list:
    #         btn_worker = InlineKeyboardButton(text=f'{worker}', callback_data=workers.new(
    #             step_menu=f'{name_step}', name=f'{worker}', name_btn='Выбрать'
    #         ))
    #         inline_kb.row(btn_worker)
    #     btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Назад'
    #     ))
    #     inline_kb.row(btn_back)
    #     return inline_kb

    # @staticmethod
    # def add_new_worker(name_step):
    #     btn_write_stage = InlineKeyboardButton(text='Добавить', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Добавить'
    #     ))
    #     btn_back = InlineKeyboardButton(text='Продолжить', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Продолжить'
    #     ))
    #     return InlineKeyboardMarkup(row_width=2).row(btn_write_stage).row(btn_back)

    # @staticmethod
    # def save_or_add_string(name_step):
    #     btn_save_form = InlineKeyboardButton(text='Сохранить форму', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Сохранить'
    #     ))
    #     btn_add_string = InlineKeyboardButton(text='Добавить строку', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Добавить'
    #     ))
    #     btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
    #         step_menu=f'{name_step}', name_btn='Назад'
    #     ))
    #     return InlineKeyboardMarkup(row_width=2).row(btn_save_form).row(btn_add_string).row(btn_back)

    @staticmethod
    def get_admin_panel_start(name_step):
        btn_get_table = InlineKeyboardButton(text='Выгрузить таблицу', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Выгрузить'
        ))
        btn_builds = InlineKeyboardButton(text='Здания', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Здания'
        ))
        btn_get_users = InlineKeyboardButton(text='Пользователи', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Пользователи'
        ))
        btn_exit = InlineKeyboardButton(text='Выйти', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Выйти'
        ))
        # return InlineKeyboardMarkup(row_width=2).row(btn_get_table).row(btn_add_user).row(btn_get_users).row(btn_exit)
        return InlineKeyboardMarkup(row_width=2).row(btn_get_users).row(btn_builds).row(btn_exit)

    @staticmethod
    def get_names_users_one_msg(step_menu: str,
                                names_users_from_db: list):
        kb_inline = InlineKeyboardMarkup(row_width=3)
        for name in names_users_from_db:
            btn_name_work = InlineKeyboardButton(text=f'{name.name}', callback_data=btn_names_msg.new(
                step_menu=step_menu, name=f'{name.user_id}', name_btn='Изменить'))
            btn_pin_code = InlineKeyboardButton(text=f'{name.password}', callback_data=btn_names_msg.new(
                step_menu=step_menu, name=f'{name.user_id}', name_btn='Изменить'))

            if not name.admin:
                btn_del = InlineKeyboardButton(text='Удалить', callback_data=btn_names_msg.new(
                    step_menu=step_menu, name=f'{name.name}', name_btn='Удалить'
                ))
                kb_inline.row(btn_name_work, btn_pin_code, btn_del)
            else:
                btn_del = InlineKeyboardButton(text=' ', callback_data=btn_names_msg.new(
                    step_menu=step_menu, name=f'{name.name}', name_btn='_'
                ))
                kb_inline.row(btn_name_work, btn_pin_code, btn_del)
        btn_add = InlineKeyboardButton(text='Добавить', callback_data=menu_callback_user.new(
            step_menu=f'{step_menu}', name_btn='Добавить'
        ))
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{step_menu}', name_btn='Назад'
        ))
        kb_inline.row(btn_add, btn_back)
        return kb_inline

    @staticmethod
    def get_all_builds(name_step: str, names_build_from_db: list):
        kb_inline = InlineKeyboardMarkup(row_width=2)
        btn_add_build = InlineKeyboardButton(text='Добавить', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Добавить'))
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'))
        for name in names_build_from_db:
            btn_name_build = InlineKeyboardButton(text=f'{name[1]}', callback_data=btn_names_msg.new(
                step_menu=name_step, name=f'{name[0]}', name_btn='Здание'))
            kb_inline.row(btn_name_build)
        kb_inline.row(btn_add_build, btn_back)
        return kb_inline

    @staticmethod
    def get_all_name_works(name_step: str, names_work: list):
        kb_inline = InlineKeyboardMarkup(row_width=2)
        btn_add_build = InlineKeyboardButton(text='Добавить', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Добавить'))
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'))
        for name in names_work:
            btn_name_build = InlineKeyboardButton(text=f'{name[0]}', callback_data=btn_names_msg.new(
                step_menu=name_step, name=f'{name[1]}', name_btn='Работа'))
            kb_inline.row(btn_name_build)
        kb_inline.row(btn_add_build, btn_back)
        return kb_inline

    @staticmethod
    def btn_change_user(name_step):
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'
        ))
        btn_change_name = InlineKeyboardButton(text='Наименование', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Наименование'
        ))
        btn_change_pin = InlineKeyboardButton(text='PIN_CODE', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='PIN_CODE'
        ))
        return InlineKeyboardMarkup(row_width=3).row(btn_change_name).row(btn_change_pin).row(btn_back)

    @staticmethod
    def btn_create_form_or_del(name_step):
        btn_create = InlineKeyboardButton(text='Создать форму', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Создать'
        ))
        btn_del = InlineKeyboardButton(text='Удалить', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Удалить'
        ))
        btn_back = InlineKeyboardButton(text='Назад', callback_data=menu_callback_user.new(
            step_menu=f'{name_step}', name_btn='Назад'
        ))
        return InlineKeyboardMarkup(row_width=2).row(btn_create, btn_del).row(btn_back)