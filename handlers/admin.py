from aiogram import types, Dispatcher
from keyboards.classic_kb import (kb_admin_panel, kb_get_table_panel,
                                  kb_btn_back, kb_finish_register_company, kb_btn_back_menu)

from aiogram.types import CallbackQuery
from keyboards.inlines_kb.callback_datas import menu_callback_user, btn_names_msg
from create_bot import dp, bot

from data_base.db_commands import CommandsDB
from keyboards.inlines_kb.kb_inlines import KBLines

from memory_FSM.bot_memory import Companies, StatesAdminUser, AuthorizationUser
from aiogram.dispatcher import FSMContext


###############################
#        СТАРТ АДМИНКИ
##############################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['AUTH_ADMIN']),
                           state=[AuthorizationUser.correct_password_admin])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['A_P_USERS']),
                           state=[StatesAdminUser.get_info_users])
async def cmd_admin_panel(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.message.edit_text('Панель управления Администратора',
                                 reply_markup=KBLines.get_admin_panel_start("ADMIN_PANEL"))
    await StatesAdminUser.start_admin_panel.set()


async def back_to_admin_panel(message: types.Message, state: FSMContext):
    await message.answer('Вы вернулись в основное меню администратора',
                         reply_markup=kb_admin_panel)
    await state.reset_state()
    await StatesAdminUser.start_admin_panel.set()


######################
#    ГЛАВНОЕ МЕНЮ
######################
async def get_table(message: types.Message):
    await message.answer('Выгрузка таблицы', reply_markup=kb_get_table_panel)
    await StatesAdminUser.get_table.set()


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Подрядчики'],
                                                     step_menu=['ADMIN_PANEL']),
                           state=[StatesAdminUser.start_admin_panel])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['DEL_USER']),
                           state=[StatesAdminUser.del_user])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['CHANGE_USER']),
                           state=[StatesAdminUser.edit_user])
async def get_information_companies(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    companies = CommandsDB.get_all_users()
    await call.message.edit_text(f'Подрядчики. Можно редактировать наименование и PINCODE\n'
                                 f'Можно удалить подрядчика',
                                 reply_markup=KBLines.get_names_users_one_msg('A_P_USERS', companies))
    await StatesAdminUser.get_info_users.set()


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Удалить'],
                                                step_menu=['A_P_USERS']),
                           state=[StatesAdminUser.get_info_users])
async def delete_user(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        name_user = callback_data['name']
        data['user_del'] = name_user
        await StatesAdminUser.del_user.set()
        await call.message.edit_text(f'Удалить компанию: {"<b>"}{name_user}{"</b>"}?',
                                     parse_mode="HTML", reply_markup=KBLines.btn_next_or_back('DEL_USER'))


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['DEL_USER']),
                           state=[StatesAdminUser.del_user])
async def accept_delete_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name_user = data['user_del']
        if CommandsDB.delete_user_with_name(name_user):
            await bot.answer_callback_query(call.id,
                                            text=f'Компания: {name_user}\n'
                                                 f'Успешно удалена!', show_alert=True)
            del data['user_del']
        await StatesAdminUser.get_info_users.set()
        companies = CommandsDB.get_all_users()
        await call.message.edit_text(f'Подрядчики. Можно редактировать наименование и PINCODE\n'
                                     f'Можно удалить подрядчика',
                                     reply_markup=KBLines.get_names_users_one_msg('A_P_USERS', companies))


# @dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
#                                                      step_menu=['CHANGE_USER_NAME']),
#                            state=[StatesAdminUser.edit_user_name])
@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Изменить'],
                                                step_menu=['A_P_USERS']),
                           state=[StatesAdminUser.get_info_users])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['SAVE_NEW_NAME', "SAVE_NEW_PIN"]),
                           state=[StatesAdminUser.edit_user_name_correct,
                                  StatesAdminUser.edit_user_pin_correct])
async def change_user(call: CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['name_btn'] == 'Назад':
        await bot.answer_callback_query(call.id)
        async with state.proxy() as data:
            await StatesAdminUser.edit_user.set()
            await call.message.edit_text(f'Выбранная компания: {"<b>"}{data["edit_user"]}{"</b>"}\n'
                                         f'Выберите поле для изменения.',
                                         parse_mode="HTML", reply_markup=KBLines.btn_change_user('CHANGE_USER'))
    else:
        await bot.answer_callback_query(call.id)
        async with state.proxy() as data:
            name_user = callback_data['name']
            data['edit_user'] = name_user
            await StatesAdminUser.edit_user.set()
            await call.message.edit_text(f'Выбранная компания: {"<b>"}{name_user}{"</b>"}\n'
                                         f'Выберите поле для изменения.',
                                         parse_mode="HTML", reply_markup=KBLines.btn_change_user('CHANGE_USER'))


######################################
#  ИЗМЕНИТЬ НАИМЕНОВАНИЕ ПОДРЯДЧИКА
#####################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Наименование'],
                                                     step_menu=['CHANGE_USER']),
                           state=[StatesAdminUser.edit_user])
async def change_user_name(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        await StatesAdminUser.edit_user_name.set()
        await call.message.edit_text(f'Текущее наименование: {"<b>"}{data["edit_user"]}{"</b>"}\n'
                                     f'Введите новое наименование до 18 символов',
                                     parse_mode="HTML", reply_markup=None)

async def write_user_name(message: types.Message, state: FSMContext):
    if len(message.text) < 19:
        async with state.proxy() as data:
            data['new_name'] = message.text
            await message.answer(f'Новое наименование: {message.text}\n'
                                 f'Сохранить?', reply_markup=KBLines.btn_next_or_back('SAVE_NEW_NAME'))
            await StatesAdminUser.edit_user_name_correct.set()
    else:
        await message.answer(f'Введенная строка: {message.text}\n'
                             f'Содержит {len(message.text)}. Необходимо ввести до 18 символов!')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['SAVE_NEW_NAME']),
                           state=[StatesAdminUser.edit_user_name_correct])
async def save_new_name_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if CommandsDB.update_name_user_with_name(data['edit_user'], data['new_name']):

            await bot.answer_callback_query(call.id, text=f'Наименование: {data["new_name"]}\n'
                                                          f'Успешно сохранено!', show_alert=True)
            data['edit_user'] = data["new_name"]
            await StatesAdminUser.edit_user.set()
            await call.message.edit_text(f'Выбранная компания: {"<b>"}{data["new_name"]}{"</b>"}\n'
                                         f'Выберите поле для изменения.',
                                         parse_mode="HTML", reply_markup=KBLines.btn_change_user('CHANGE_USER'))


#########################
#    ИЗМЕНИТЬ ПАРОЛЬ
#########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['PIN_CODE'],
                                                     step_menu=['CHANGE_USER']),
                           state=[StatesAdminUser.edit_user])
async def change_user_pin(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        data['edit_pin'] = CommandsDB.get_password_user_with_name(data['edit_user'])
        await StatesAdminUser.edit_user_pin.set()
        await call.message.edit_text(f'Текущий PIN_CODE: {"<b>"}{data["edit_pin"]}{"</b>"}\n'
                                     f'Введите новый PIN_CODE.\n'
                                     f'Требования: только цифры от 4 до 6 символов, без пробелов.',
                                     parse_mode="HTML", reply_markup=None)

async def write_user_pin(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        if 4 <= len(message.text) <= 6:
            if message.text not in CommandsDB.get_all_users(user_password=True):
                async with state.proxy() as data:
                    data['new_pin'] = message.text
                    await message.answer(f'Новый PIN_CODE: {message.text}\n'
                                         f'Сохранить?', reply_markup=KBLines.btn_next_or_back('SAVE_NEW_PIN'))
                    await StatesAdminUser.edit_user_pin_correct.set()
            else:
                await message.answer(f'Введенный PIN_CODE: {message.text}\n'
                                     f'Уже есть в системе. Введите другой PIN_CODE!')
        else:
            await message.answer(f'Введенная строка: {message.text}\n'
                                 f'PIN_CODE не подходит по длине!')
    else:
        await message.answer(f'Введенная строка: {message.text}\n'
                             f'PIN_CODE должен содержать только цифры!')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['SAVE_NEW_PIN']),
                           state=[StatesAdminUser.edit_user_pin_correct])
async def save_new_pin_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if CommandsDB.update_pincode_user_with_name(data['edit_user'], data['new_pin']):
            await bot.answer_callback_query(call.id, text=f'PIN_CODE: {data["new_pin"]}\n'
                                                          f'Успешно сохранен!', show_alert=True)
            await StatesAdminUser.edit_user.set()
            await call.message.edit_text(f'Выбранная компания: {"<b>"}{data["edit_user"]}{"</b>"}\n'
                                         f'Выберите поле для изменения.',
                                         parse_mode="HTML", reply_markup=KBLines.btn_change_user('CHANGE_USER'))

###############################
# Создание нового пользователя
###############################

async def write_company_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['company_name'] = message.text

    if CommandsDB.get_count(message.text) != 0:
        await message.answer(f"Пользователь {message.text} уже есть в системе \n"
                             f"Введите новое имя или нажмите кнопку Назад")
        await StatesAdminUser.add_user.set()
    else:
        await StatesAdminUser.write_user_name.set()
        await message.answer('Введите комментарий к компании', reply_markup=kb_btn_back)


async def write_company_comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text
    await StatesAdminUser.write_user_comment.set()
    await message.answer(f'Сохранить компанию?\n'
                         f'Наименование: {data["company_name"]}\n'
                         f'Комментарий: {data["comment"]}\n',
                         reply_markup=kb_finish_register_company)


async def save_new_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['save'] = True
    await StatesAdminUser.save_user.set()
    CommandsDB.add_user_system(name=data['company_name'],
                               comment=data['comment'])
    await message.answer(f"Компания: {data['company_name']}\n"
                         f"Комментарий: {data['comment']}"
                         f"\n Сохранена",
                         reply_markup=kb_btn_back_menu)


########################################
#
########################################

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(write_user_name, state=StatesAdminUser.edit_user_name)
    dp.register_message_handler(write_user_pin, state=StatesAdminUser.edit_user_pin)
    # dp.register_message_handler(back_to_admin_panel, lambda message: 'В главное меню' in message.text,
    #                             state=[StatesAdminUser.save_user])
    ############################
    # Отмена Назад Главное меню
    ############################
    # dp.register_message_handler(back_to_admin_panel, lambda message: 'Назад' in message.text,
    #                             state=[
    #                                 Companies.list_companies,
    #                                 StatesAdminUser.get_table,
    #                                 StatesAdminUser.add_user,
    #                                 StatesAdminUser.write_user_name,
    #                                 StatesAdminUser.write_user_comment,
    #                                 StatesAdminUser.get_info_users
    #                             ])
    # dp.register_message_handler(back_to_admin_panel, lambda message: 'Отменить' in message.text,
    #                             state=[StatesAdminUser.write_user_comment])
    # dp.register_message_handler(back_to_admin_panel, lambda message: 'В главное меню' in message.text,
    #                             state=[StatesAdminUser.save_user])
    #
    # #############################
    # #       ГЛАВНОЕ МЕНЮ
    # #############################
    # dp.register_message_handler(cmd_admin_panel, lambda message: 'Ген_подрядчик' in message.text)
    # dp.register_message_handler(get_table, lambda message: 'Выгрузить таблицу' in message.text,
    #                             state=StatesAdminUser.start_admin_panel)
    # dp.register_message_handler(get_information_companies, lambda message: 'Информация об орг-ях' in message.text,
    #                             state=StatesAdminUser.start_admin_panel)
    # dp.register_message_handler(add_company_user, lambda message: 'Добавить Подрядчика' in message.text,
    #                             state=StatesAdminUser.start_admin_panel)
    #
    # ##############################
    # #    ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
    # ##############################
    # dp.register_message_handler(write_company_name, state=StatesAdminUser.add_user)
    # dp.register_message_handler(write_company_comment, state=StatesAdminUser.write_user_name)
    # dp.register_message_handler(save_new_user, lambda message: 'Сохранить' in message.text,
    #                             state=StatesAdminUser.write_user_comment)
