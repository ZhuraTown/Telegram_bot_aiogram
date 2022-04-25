from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

delete_callback = CallbackData('callback_delete', 'name_company', 'id_company', 'command')

workers_callback = CallbackData('workers', 'type_step', 'type_worker', 'amount')
menu_callback = CallbackData('menu_btn', 'btn_menu', 'type_btn')

add_users = CallbackData('add_users', 'type', "type_user")
minus_users = CallbackData('add_users', 'type', "type_user")

none_callback = CallbackData('none_callback', 'none_call')

