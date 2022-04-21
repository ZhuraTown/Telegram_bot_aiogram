from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


##########################
#   DELETE_KB
##########################
kb_delete = ReplyKeyboardRemove()
###########################
#          START
###########################
kb_gen = KeyboardButton('Ген_подрядчик')
kb_users = KeyboardButton('Подрядчики')

kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_start.row(kb_users, kb_gen)
############################
#      ADMIN_PANEL
############################
btn_get_tb = KeyboardButton("Выгрузить таблицу")
btn_add_user = KeyboardButton("Добавить Подрядчика")
btn_edit_user = KeyboardButton("Редактировать Подрядчиков")
btn_get_info_users = KeyboardButton("Информация об орг-ях")
btn_back = KeyboardButton("Назад")
btn_exit = KeyboardButton("Выйти")
btn_back_menu = KeyboardButton('В главное меню')

kb_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_admin_panel.row(btn_get_tb, btn_add_user).row(btn_get_info_users, btn_exit)

############################
#          GET TABLE
###########################
btn_get_table_today = KeyboardButton("Таблица за Сегодня")
btn_get_table_date = KeyboardButton("Таблица за Дату")
kb_get_table_panel = ReplyKeyboardMarkup(resize_keyboard=True).row(btn_get_table_today, btn_get_table_date, btn_back)

############################
#       USER_PANEL
############################
btn_user_create_form = KeyboardButton("Заполнить форму")
btn_user_edit_form = KeyboardButton("Редактировать форму")
kb_user_panel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_user_panel.row(btn_user_create_form, btn_user_edit_form, btn_back)

############################
#       CREATE_FORM
############################
btn_write_name_work = KeyboardButton('Ввести наименование работ')
btn_choose_name_work = KeyboardButton('Выбрать наименование работ')
btn_form_back = KeyboardButton('Назад')
kb_form_name_work = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(btn_write_name_work, btn_choose_name_work).row(btn_form_back)

btn_save = KeyboardButton('Сохранить')
btn_cancel = KeyboardButton('Отменить')
kb_finish_register_company = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(btn_save, btn_cancel)

##########################
#         BACK
#########################
kb_btn_back = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_back)
kb_btn_back_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_back_menu)