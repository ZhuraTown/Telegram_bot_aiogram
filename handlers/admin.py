from aiogram import types, Dispatcher
from keyboards.classic_kb import (kb_admin_panel, kb_get_table_panel,
                                  kb_btn_back, kb_finish_register_company, kb_start)
from keyboards.inline_kb import edit_company
from aiogram.dispatcher import FSMContext

from memory_FSM.bot_memory import StatesAdmin, RegisterUser, Companies


async def cmd_admin_panel(message: types.Message):
    await message.answer('Панель управления Ген подрядчика', reply_markup=kb_admin_panel)


async def back_to_admin_panel(message: types.Message, state: FSMContext):
    await message.answer('Вы вернулись в основное меню администратора', reply_markup=kb_admin_panel)
    await state.reset_state()


async def get_table(message: types.Message):
    await message.answer('Выгрузка таблицы', reply_markup=kb_get_table_panel)
    await StatesAdmin.admin_table_menu.set()


###############################
# Создание нового пользователя
###############################
async def add_company_user(message: types.Message):
    await RegisterUser.write_name.set()
    await message.answer('Введите наименование компании', reply_markup=kb_btn_back)


async def write_company_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['company_name'] = message.text
    await RegisterUser.write_comment.set()
    await message.answer('Введите комментарий к компании', reply_markup=kb_btn_back)


async def write_company_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text
    await RegisterUser.add_or_delete.set()
    await message.answer(f'Сохранить компанию?\n'
                         f'Наименование: {data["company_name"]}\n'
                         f'Комментарий: {data["comment"]}\n'
                         f'PIN_CODE: 23123123', reply_markup=kb_finish_register_company)


async def get_information_companies(message: types.Message):
    companies = ['Первая', 'EST', 'LIIS']
    for company in companies:
        await message.answer(f'Наименование: {company} \n Комментарий ПОТОМ ДОБАВЛЮ'
                             f'\n PIN_CODE: 123124124', reply_markup=edit_company)
    await Companies.list_companies.set()
    await message.answer("Информация об организациях. Выберите действие или вернитесь назад", reply_markup=kb_btn_back)


async def exit_to_main_menu(message: types.Message, state: FSMContext):
    await message.delete()
    await state.reset_state()
    await message.answer('Цель бота, упростить заполнение табеля рабочего времени сотрудников Лахта Центр\n'
                         'Введите PIN_CODE для входа в личный кабинет', reply_markup=kb_start)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(back_to_admin_panel, lambda message: 'Назад' in message.text,
                                state=[StatesAdmin.admin_table_menu,
                                       RegisterUser.write_comment,
                                       RegisterUser.write_name,
                                       RegisterUser.add_or_delete,
                                       Companies.list_companies])
    dp.register_message_handler(cmd_admin_panel, lambda message: 'Ген_подрядчик' in message.text)
    dp.register_message_handler(get_table, lambda message: 'Выгрузить таблицу' in message.text)
    dp.register_message_handler(add_company_user, lambda message: 'Добавить Подрядчика' in message.text, state=None)
    dp.register_message_handler(get_information_companies, lambda message: 'Информация об орг-ях' in message.text, state=None)
    dp.register_message_handler(exit_to_main_menu, lambda message: 'Выйти' in message.text)
    dp.register_message_handler(write_company_name, state=RegisterUser.write_name)
    dp.register_message_handler(write_company_comment, state=RegisterUser.write_comment)
