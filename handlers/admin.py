import datetime
import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile

from create_bot import dp, bot
from data_base.db_commands import CommandsDB
from keyboards.inlines_kb.callback_datas import menu_callback_user, btn_names_msg
from keyboards.inlines_kb.kb_inlines import KBLines
from memory_FSM.bot_memory import StatesAdminUser, AuthorizationUser



###############################
#        СТАРТ АДМИНКИ
##############################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['AUTH_ADMIN']),
                           state=[AuthorizationUser.correct_password_admin])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['A_P_USERS', "BUILDS", "TABLE_TIME"]),
                           state=[StatesAdminUser.get_info_users,
                                  StatesAdminUser.user_name_correct, StatesAdminUser.builds, StatesAdminUser.get_table])
async def cmd_admin_panel(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id, cache_time=5)
    await state.reset_state()
    await call.message.edit_text('Панель управления Администратора',
                                 reply_markup=KBLines.get_admin_panel_start("ADMIN_PANEL"))
    await StatesAdminUser.start_admin_panel.set()


######################
#    ГЛАВНОЕ МЕНЮ
######################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['ГП'],
                                                     step_menu=['ADMIN_PANEL']),
                           state=[StatesAdminUser.start_admin_panel])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['DEL_USER']),
                           state=[StatesAdminUser.del_user])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['CHANGE_USER', "NAME_USER"]),
                           state=[StatesAdminUser.edit_user, StatesAdminUser.user_name_correct])
async def get_information_companies(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    companies = CommandsDB.get_all_users(contractor=True)
    await call.message.edit_text(f'Можно редактировать/добавлять Ген Подрядчиков',
                                 reply_markup=KBLines.get_names_users_one_msg('A_P_USERS', companies))
    await StatesAdminUser.get_info_users.set()


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Удалить'],
                                                step_menu=['A_P_USERS']),
                           state=[StatesAdminUser.get_info_users])
async def delete_user(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        name_user = CommandsDB.get_user_with_id(callback_data['name'])[0]
        data['user_del_id'] = callback_data['name']
        data['user_del_name'] = name_user
        await StatesAdminUser.del_user.set()
        await call.message.edit_text(f'Удалить ГП: {"<b>"}{name_user}{"</b>"}?',
                                     parse_mode="HTML", reply_markup=KBLines.btn_next_or_back('DEL_USER'))


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['DEL_USER']),
                           state=[StatesAdminUser.del_user])
async def accept_delete_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        id_user = data['user_del_id']
        name_user = data['user_del_name']
        if CommandsDB.delete_user_with_id(id_user):
            await bot.answer_callback_query(call.id,
                                            text=f'Ген.Подрядчик: {name_user}\n'
                                                 f'Успешн удален!', show_alert=True)
            del data['user_del']
            del data['user_del_id']
        await StatesAdminUser.get_info_users.set()
        companies = CommandsDB.get_all_users(contractor=True)
        await call.message.edit_text(f'Можно редактировать наименование и PINCODE\n'
                                     f'Можно удалить ГП.',
                                     reply_markup=KBLines.get_names_users_one_msg('A_P_USERS', companies))


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
            await call.message.edit_text(f'Выбран Ген Подрядчик: {"<b>"}{data["edit_user"]}{"</b>"}\n'
                                         f'Выберите поле для изменения.',
                                         parse_mode="HTML", reply_markup=KBLines.btn_change_user('CHANGE_USER'))
    else:
        await bot.answer_callback_query(call.id)
        async with state.proxy() as data:
            name_user = CommandsDB.get_user_with_id(callback_data['name'])[0]
            data['edit_user'] = name_user
            data['edit_user_id'] = callback_data['name']
            await StatesAdminUser.edit_user.set()
            await call.message.edit_text(f'Выбран Ген Подрядчик: {"<b>"}{data["edit_user"]}{"</b>"}\n'
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
            await message.answer(f'Новое наименование: {"<b>"}{message.text}{"</b>"}\n'
                                 f'Сохранить?', reply_markup=KBLines.btn_next_or_back('SAVE_NEW_NAME'),
                                 parse_mode='HTML')
            await StatesAdminUser.edit_user_name_correct.set()
    else:
        await message.answer(f'Введенная строка: {message.text}\n'
                             f'Содержит {len(message.text)}. Необходимо ввести до 18 символов!')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['SAVE_NEW_NAME']),
                           state=[StatesAdminUser.edit_user_name_correct])
async def save_new_name_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if CommandsDB.update_gp_user_with_name(data['edit_user'], data['new_name']):
            await bot.answer_callback_query(call.id, text=f'Наименование: {"<b>"}{data["new_name"]}{"/<b>"}\n'
                                                          f'Успешно сохранено!', show_alert=True)
            data['edit_user'] = data["new_name"]
            await StatesAdminUser.edit_user.set()
            await call.message.edit_text(f'Выбран Ген Подрядчик: {"<b>"}{data["new_name"]}{"</b>"}\n'
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
                    await message.answer(f'Новый PIN_CODE: {"<b>"}{message.text}{"</b>"}\n'
                                         f'Сохранить?', reply_markup=KBLines.btn_next_or_back('SAVE_NEW_PIN'),
                                         parse_mode="HTML")
                    await StatesAdminUser.edit_user_pin_correct.set()
            else:
                await message.answer(f'Введенный PIN_CODE: {"<b>"}{message.text}{"</b>"}\n'
                                     f'Уже есть в системе. Введите другой PIN_CODE!',
                                     parse_mode='HTML')
        else:
            await message.answer(f'Введенная строка: {"<b>"}{message.text}{"</b>"}\n'
                                 f'PIN_CODE не подходит по длине!',
                                 parse_mode="HTML")
    else:
        await message.answer(f'Введенная строка: {"<b>"}{message.text}{"</b>"}\n'
                             f'PIN_CODE должен содержать только цифры!',
                             parse_mode="HTML")


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['SAVE_NEW_PIN']),
                           state=[StatesAdminUser.edit_user_pin_correct])
async def save_new_pin_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        # if CommandsDB.update_pincode_user_with_name(data['edit_user'], data['new_pin']):
        if CommandsDB.update_pincode_user_with_name(data['edit_user_id'], data['new_pin']):
            await bot.answer_callback_query(call.id, text=f'PIN_CODE: {data["new_pin"]}\n'
                                                          f'Успешно сохранен!', show_alert=True)
            await StatesAdminUser.edit_user.set()
            await call.message.edit_text(f'Выбранный Ген Подрядчик: {"<b>"}{data["edit_user"]}{"</b>"}\n'
                                         f'Выберите поле для изменения.',
                                         parse_mode="HTML", reply_markup=KBLines.btn_change_user('CHANGE_USER'))


###############################
# Создание нового пользователя
###############################

@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить'],
                                                     step_menu=['A_P_USERS']),
                           state=[StatesAdminUser.get_info_users])
async def create_new_user(call: CallbackQuery):
    await bot.answer_callback_query(call.id, cache_time=5)
    await call.message.edit_text(f'Создать нового пользователя\n'
                                 f'Кнопка Назад появится после ввода любого текста', reply_markup=None)
    await StatesAdminUser.write_user_name.set()


async def write_name_user(message: types.Message, state: FSMContext):
    names_user = CommandsDB.get_all_gp()
    if message.text not in names_user:
        if len(message.text) < 19:
            async with state.proxy() as data:
                data['new_name_user'] = message.text
            await message.answer(f'Имя Ген Подрядчика: {"<b>"}{message.text}{"</b>"}\n'
                                 f'Сохранить?', parse_mode='HTML',
                                 reply_markup=KBLines.btn_next_or_back('NAME_USER'))
            await StatesAdminUser.user_name_correct.set()
        else:
            await message.answer(f'Длина введенного имени({"<b>"}{message.text}{"</b>"})\n'
                                 f'{len(message.text)}. Введите не более 18 символов', parse_mode="HTML")
    else:
        await message.answer(f'Имя пользователя({"<b>"}{message.text}{"</b>"}) уже есть в системе!\n'
                             f'Введите имя пользователя, которого нету в системе.', parse_mode='HTML')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['NAME_USER']),
                           state=[StatesAdminUser.user_name_correct])
async def save_new_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pin_codes_db = CommandsDB.get_all_users(user_password=True)
        pin_code_user = random.randint(1000, 9999)
        while pin_code_user in pin_codes_db:
            pin_code_user = random.randint(1000, 9999)
        # Создаём пользователя
        if CommandsDB.add_get_contractor(data['new_name_user'], pin_code_user):
            await bot.answer_callback_query(call.id,
                                            text=f'Ген Подрядчик:{data["new_name_user"]}\n'
                                                 f'Успешно добавлен в систему!', show_alert=True)
        else:
            await bot.answer_callback_query(call.id,
                                            text=f'Не удалось добавить пользователя: {data["new_name_user"]}'
                                                 f'в систему!', show_alert=True)
        await state.reset_state()
        await call.message.edit_text('Панель управления Администратора',
                                     reply_markup=KBLines.get_admin_panel_start("ADMIN_PANEL"))
        await StatesAdminUser.start_admin_panel.set()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(write_user_name, state=StatesAdminUser.edit_user_name)
    dp.register_message_handler(write_user_pin, state=StatesAdminUser.edit_user_pin)
    dp.register_message_handler(write_name_user, state=StatesAdminUser.write_user_name)
