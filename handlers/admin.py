from aiogram import types, Dispatcher
from keyboards.classic_kb import (kb_admin_panel, kb_get_table_panel,
                                  kb_btn_back, kb_finish_register_company, kb_btn_back_menu)
from keyboards.inline_kb import edit_company
from aiogram.dispatcher import FSMContext

from memory_FSM.bot_memory import Companies, StatesAdminUser


async def cmd_admin_panel(message: types.Message):
    await message.answer('Панель управления Ген подрядчика', reply_markup=kb_admin_panel)
    await StatesAdminUser.start_admin_panel.set()


async def back_to_admin_panel(message: types.Message, state: FSMContext):
    await message.answer('Вы вернулись в основное меню администратора', reply_markup=kb_admin_panel)
    await state.reset_state()
    await StatesAdminUser.start_admin_panel.set()


######################
#    ГЛАВНОЕ МЕНЮ
######################
async def get_table(message: types.Message):
    await message.answer('Выгрузка таблицы', reply_markup=kb_get_table_panel)
    # await StatesAdmin.admin_table_menu.set()
    await StatesAdminUser.get_table.set()


async def get_information_companies(message: types.Message):
    await StatesAdminUser.get_info_users.set()
    companies = ['Первая', 'EST', 'LIIS']
    for company in companies:
        await message.answer(f'Наименование: {company} \n Комментарий ПОТОМ ДОБАВЛЮ'
                             f'\n PIN_CODE: 123124124', reply_markup=edit_company)
    await Companies.list_companies.set()
    await message.answer("Информация об организациях. Выберите действие или вернитесь назад", reply_markup=kb_btn_back)


async def add_company_user(message: types.Message):
    await message.answer('Введите наименование компании', reply_markup=kb_btn_back)
    await StatesAdminUser.add_user.set()


###############################
# Создание нового пользователя
###############################


async def write_company_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['company_name'] = message.text
    await StatesAdminUser.write_user_name.set()
    await message.answer('Введите комментарий к компании', reply_markup=kb_btn_back)


async def write_company_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text
    await StatesAdminUser.write_user_comment.set()
    await message.answer(f'Сохранить компанию?\n'
                         f'Наименование: {data["company_name"]}\n'
                         f'Комментарий: {data["comment"]}\n'
                         f'PIN_CODE: 23123123', reply_markup=kb_finish_register_company)


async def save_new_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['save'] = True
    await StatesAdminUser.save_user.set()
    await message.answer(f"Компания\n{data['company_name']}\n{data['comment']}\n Сохранена",
                         reply_markup=kb_btn_back_menu)


########################################
#
########################################

def register_handlers_admin(dp: Dispatcher):
    ############################
    # Отмена Назад Главное меню
    ############################
    dp.register_message_handler(back_to_admin_panel, lambda message: 'Назад' in message.text,
                                state=[
                                    Companies.list_companies,
                                    StatesAdminUser.get_table,
                                    StatesAdminUser.add_user,
                                    StatesAdminUser.write_user_name,
                                    StatesAdminUser.write_user_comment,
                                    StatesAdminUser.get_info_users
                                ])
    dp.register_message_handler(back_to_admin_panel, lambda message: 'Отменить' in message.text,
                                state=[StatesAdminUser.write_user_comment])
    dp.register_message_handler(back_to_admin_panel, lambda message: 'В главное меню' in message.text,
                                state=[StatesAdminUser.save_user])

    #############################
    #       ГЛАВНОЕ МЕНЮ
    #############################
    dp.register_message_handler(cmd_admin_panel, lambda message: 'Ген_подрядчик' in message.text)
    dp.register_message_handler(get_table, lambda message: 'Выгрузить таблицу' in message.text,
                                state=StatesAdminUser.start_admin_panel)
    dp.register_message_handler(get_information_companies, lambda message: 'Информация об орг-ях' in message.text,
                                state=StatesAdminUser.start_admin_panel)
    dp.register_message_handler(add_company_user, lambda message: 'Добавить Подрядчика' in message.text,
                                state=StatesAdminUser.start_admin_panel)

    ##############################
    #    ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
    ##############################
    dp.register_message_handler(write_company_name, state=StatesAdminUser.add_user)
    dp.register_message_handler(write_company_comment, state=StatesAdminUser.write_user_name)
    dp.register_message_handler(save_new_user, lambda message: 'Сохранить' in message.text,
                                state=StatesAdminUser.write_user_comment)
