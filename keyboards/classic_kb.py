from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

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
btn_get_tb_today = KeyboardButton("Таблица сегодня")
btn_get_tb_date = KeyboardButton("Таблица за дату")
btn_add_user = KeyboardButton("Добавить Подрядчика")
btn_edit_user = KeyboardButton("Редактировать Подрядчиков")
btn_get_info_users = KeyboardButton("Информация об орг-ях")
btn_back = KeyboardButton("Назад")

kb_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin_panel.row(btn_get_tb_today,
                   btn_get_tb_date, btn_add_user).row(btn_get_info_users, btn_back)
############################
#       USER_PANEL
############################
btn_user_create_form = KeyboardButton("Заполнить форму")
btn_user_edit_form = KeyboardButton("Редактировать форму")
kb_user_panel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_user_panel.row(btn_user_create_form, btn_user_edit_form, btn_back)



