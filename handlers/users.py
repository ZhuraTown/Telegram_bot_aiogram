from aiogram import types, Dispatcher
from create_bot import dp
from keyboards.classic_kb import kb_user_panel, kb_form_name_work, kb_btn_back


async def cmd_users_panel(message: types.Message):
    await message.delete()
    await message.answer('Панель управления Подрядчика', reply_markup=kb_user_panel)


async def create_form(message: types.Message):
    await message.delete()
    await message.answer('Заполнение формы \n Выберите следующий шаг', reply_markup=kb_form_name_work)


async def write_name_work(message: types.Message):
    await message.delete()
    await message.answer('Введите наименование работ', reply_markup=kb_user_panel)


async def choice_name_work(message: types.Message):
    await message.delete()
    for i in range(1, 10):
        await message.answer(f'Наименование работы,\n наименование: {i}', reply_markup=types.InlineKeyboardMarkup(row_width=1).
                             add(types.InlineKeyboardButton(text=f'Выбрать', callback_data=f'nw_{i}')))
    await message.answer("Выберите наименование работ, \n или вернитесь Назад", reply_markup=kb_btn_back)


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(cmd_users_panel, lambda message: 'Подрядчики' in message.text)
    dp.register_message_handler(create_form, lambda message: 'Заполнить' in message.text)
    dp.register_message_handler(write_name_work, lambda message: 'Введите наименование работ' in message.text)
    dp.register_message_handler(choice_name_work, lambda message: 'Выбрать наименование работ' in message.text)
