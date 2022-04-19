from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_inline_kb = InlineKeyboardMarkup(row_width=1).row(
    InlineKeyboardButton(text='Подрядчик', callback_data='start_user'),
    InlineKeyboardButton(text='Ген_Подрядчик', callback_data='start_admin_user'))

user_inline_panel = InlineKeyboardMarkup(row_width=1).row(
    InlineKeyboardButton(text='Заполинть форму', callback_data='write_form'),
    InlineKeyboardButton(text='Редактировать форму', callback_data='edit_form'),
    InlineKeyboardButton(text="Назад", callback_data='back_user_panel'))


edit_company = InlineKeyboardMarkup(row_width=1).row(
    InlineKeyboardButton(text='Редактировать', callback_data='edit_company'),
    InlineKeyboardButton(text='Удалить', callback_data='del_company'),
)

