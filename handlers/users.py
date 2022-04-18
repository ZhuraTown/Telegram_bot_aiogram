from aiogram import types, Dispatcher
from create_bot import dp
from keyboards.classic_kb import kb_start, kb_admin_panel, kb_user_panel
from keyboards.inline_kb import inline_kb

######################################################################
#                           КЛИЕНТСКАЯ ЧАСТь
######################################################################
async def command_start(message: types.Message):
    await message.delete()
    await message.answer('Цель бота, упростить заполнение табеля рабочего времени сотрудников Лахта Центр\n'
                         'Введите PIN_CODE для входа в личный кабинет', reply_markup=kb_start)


async def command_help(message: types.Message):
    await message.answer('ПОМОЩЬ ПОДСКАЗКИ')


async def cmd_admin_panel(message: types.Message):
    await message.answer('Панель управления Ген подрядчика', reply_markup=kb_admin_panel)


async def cmd_users_panel(message: types.Message):
    await message.answer('Панель управления Подрядчика', reply_markup=kb_user_panel)


async def create_form(message: types.Message):
    await message.answer('Заполнение формы \n Введите наименование работ', reply_markup=inline_kb)


async def create_form_callback_query(callback: types.CallbackQuery):
    await callback.message.answer('Начата заполнение формы. Введите наименование работ', reply_markup=inline_kb)


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(cmd_admin_panel, lambda message: 'Ген_подрядчик' in message.text)
    dp.register_message_handler(cmd_users_panel, lambda message: 'Подрядчик' in message.text)
    dp.register_message_handler(cmd_users_panel, lambda message: 'Подрядчик' in message.text)
    dp.register_message_handler(create_form, lambda message: 'Заполнить' in message.text)
    dp.register_callback_query_handler(create_form_callback_query, 'ttt_1')