import datetime
import random

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ParseMode
from aiogram.utils.markdown import hlink

from create_bot import dp, bot
from data_base.db_commands import CommandsDB
from keyboards.inlines_kb.callback_datas import menu_callback_user, btn_names_msg
from keyboards.inlines_kb.kb_inlines import KBLines
from memory_FSM.bot_memory import StatesUsers, AuthorizationUser
from flask_server.generator_url import GeneratorUrlFlask
from excel_creator.excel_writer import ExcelWriter


def except_raise(func):
    async def wrapper():
        try:
            return await func()
        except Exception as e:
            print(f'Ошибка {e}')
            
    return wrapper


########################
#      ГЛАВНОЕ МЕНЮ
########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['AUTH_USER']),
                           state=[AuthorizationUser.correct_password_user])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['WRITE_FORM', "SEE_FORM", 'A_P_USERS', "BUILDS",
                                                                "TABLE_TIME"]),
                           state=[StatesUsers.create_new_form, StatesUsers.get_forms,
                                  StatesUsers.get_info_users, StatesUsers.builds, StatesUsers.get_table])
async def cmd_users_panel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    async with state.proxy() as data:
        if data['is_GP']:
            await call.message.edit_text(f'Добро пожаловать в панель управления ГП\n'
                                         f'Вы авторизовались как {"<b>"}{data["user_name"]}{"</b>"}',
                                         parse_mode=ParseMode.HTML, reply_markup=KBLines.get_start_panel_gp())
        else:
            await call.message.edit_text(f'Добро пожаловать в панель управления подрядчика\n'
                                         f'Ген подрядчик: {"<b>"}{data["GP"]}{"</b>"}\n'
                                         f'Вы авторизовались как {"<b>"}{data["user_name"]}{"</b>"}',
                                         parse_mode=ParseMode.HTML, reply_markup=KBLines.get_start_panel_btn())
        await StatesUsers.start_user_panel.set()


#############################
#    ВЫГРУЗИТЬ ТАБЛИЦЫ
#############################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Таблица'],
                                                     step_menu=['USER_MAIN_PAGE']),
                           state=[StatesUsers.start_user_panel])
async def get_table_time_sheet(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        date_today = datetime.datetime.today().date()
        await StatesUsers.get_table.set()
        await call.message.edit_text(f'Таблица подрядчиков за:{"<b>"}{date_today}{"</b>"}',
                                     parse_mode='HTML', reply_markup=None)
        gp_name = data['user_name']
        gp_id = data['id_user']

        tb_sheet = ExcelWriter('Отчет_по_табелю')
        path_to_file = tb_sheet.get_path_to_file()

        stages = CommandsDB.get_stages_today_from_form(gp_id)
        comps_and_work = CommandsDB.get_names_work_companies_from_form(gp_id)
        tb_sheet.create_table_header(gp_name, stages, len(comps_and_work))
        # Заполнение Этап, Здание, Этаж, Ген подрядчик
        lns_from_form_with_contactor = CommandsDB.get_all_str_from_form_with_cont(gp_id)
        tb_sheet.write_companies_to_tb(comps_and_work)
        tb_sheet.write_title_tb_tm_sh()
        tb_sheet.write_title_companies_tb(comps_and_work)
        tb_sheet.write_builds_st_lv_tb(lns_from_form_with_contactor)
        tb_sheet.write_nums_workers(lns_from_form_with_contactor)
        tb_sheet.write_results_formulas_bottom()
        tb_sheet.write_results_formulas_right()
        tb_sheet.write_total_nums_works_to_tb(comps_and_work)
        tb_sheet.close()
        file = open(path_to_file, 'rb')
        await bot.send_document(call.message.chat.id, file)
        await bot.send_message(call.message.chat.id, 'Нажмите кнопку Назад, чтобы вернутся в меню',
                               reply_markup=KBLines.btn_back('TABLE_TIME'))


###########################
#       Подрядчики
###########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Подрядчики'],
                                                     step_menu=['USER_MAIN_PAGE']),
                           state=[StatesUsers.start_user_panel])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['DEL_USER']),
                           state=[StatesUsers.del_user])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['CHANGE_USER', "NAME_USER"]),
                           state=[StatesUsers.edit_user, StatesUsers.user_name_correct])
async def get_information_companies(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await bot.answer_callback_query(call.id)
        companies = CommandsDB.get_all_users(gp=data['user_name'], gp_id=data['id_user'])
        await call.message.edit_text(f'Панель управления подрядчиками',
                                     reply_markup=KBLines.get_names_users_one_msg('A_P_USERS', companies))
        await StatesUsers.get_info_users.set()


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Удалить'],
                                                step_menu=['A_P_USERS']),
                           state=[StatesUsers.get_info_users])
async def delete_user(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        name_user = CommandsDB.get_user_with_id(callback_data['name'])[0]
        data['user_del_id'] = callback_data['name']
        data['user_del_name'] = name_user
        await StatesUsers.del_user.set()
        await call.message.edit_text(f'Удалить подрядчика: {"<b>"}{name_user}{"</b>"}?',
                                     parse_mode="HTML", reply_markup=KBLines.btn_next_or_back('DEL_USER'))


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['DEL_USER']),
                           state=[StatesUsers.del_user])
async def accept_delete_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        id_user = data['user_del_id']
        name_user = data['user_del_name']
        if CommandsDB.delete_user_with_id(id_user):
            await bot.answer_callback_query(call.id,
                                            text=f'Подрядчик: {name_user}\n'
                                                 f'Успешно удален!', show_alert=True)
            del data['user_del']
        await StatesUsers.get_info_users.set()
        companies = CommandsDB.get_all_users(gp=data['user_name'], gp_id=data['id_user'])
        await call.message.edit_text(f'Панель управления подрядчиками',
                                     reply_markup=KBLines.get_names_users_one_msg('A_P_USERS', companies))


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Изменить'],
                                                step_menu=['A_P_USERS']),
                           state=[StatesUsers.get_info_users])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['SAVE_NEW_NAME', "SAVE_NEW_PIN"]),
                           state=[StatesUsers.edit_user_name_correct,
                                  StatesUsers.edit_user_pin_correct])
async def change_user(call: CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data['name_btn'] == 'Назад':
        await bot.answer_callback_query(call.id)
        async with state.proxy() as data:
            await StatesUsers.edit_user.set()
            await call.message.edit_text(f'Выбран подрядчик: {"<b>"}{data["edit_user"]}{"</b>"}\n'
                                         f'Выберите поле для изменения.',
                                         parse_mode="HTML", reply_markup=KBLines.btn_change_user('CHANGE_USER'))
    else:
        await bot.answer_callback_query(call.id)
        async with state.proxy() as data:

            name_user = CommandsDB.get_user_with_id(callback_data['name'])[0]
            data['edit_user_id'] = callback_data['name']
            data['edit_user'] = name_user
            await StatesUsers.edit_user.set()
            await call.message.edit_text(f'Выбран подрядчик: {"<b>"}{data["edit_user"]}{"</b>"}\n'
                                         f'Выберите поле для изменения.',
                                         parse_mode="HTML", reply_markup=KBLines.btn_change_user('CHANGE_USER'))


######################################
#  ИЗМЕНИТЬ НАИМЕНОВАНИЕ ПОДРЯДЧИКА
#####################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Наименование'],
                                                     step_menu=['CHANGE_USER']),
                           state=[StatesUsers.edit_user])
async def change_user_name(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        await StatesUsers.edit_user_name.set()
        await call.message.edit_text(f'Текущее наименование: {"<b>"}{data["edit_user"]}{"</b>"}\n'
                                     f'Введите новое наименование до 18 символов',
                                     parse_mode="HTML", reply_markup=None)


async def write_user_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        names_user = CommandsDB.get_all_user_with_gp(data['user_name'])
        if message.text not in names_user:
            if len(message.text) < 19:
                data['new_name'] = message.text
                await message.answer(f'Новое наименование: {message.text}\n'
                                     f'Сохранить?', reply_markup=KBLines.btn_next_or_back('SAVE_NEW_NAME'))
                await StatesUsers.edit_user_name_correct.set()
            else:
                await message.answer(f'Введенная строка: {message.text}\n'
                                     f'Содержит {len(message.text)}. Необходимо ввести до 18 символов!')
        else:
            await message.answer(f'Подрядчик с именем({"<b>"}{message.text}{"</b>"}) уже есть в системе!\n'
                                 f'Введите другое имя, которого нету в системе.', parse_mode='HTML')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['SAVE_NEW_NAME']),
                           state=[StatesUsers.edit_user_name_correct])
async def save_new_name_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if CommandsDB.update_name_user_with_gp_with_name(data['edit_user_id'], data['new_name'], data['user_name']):
            await bot.answer_callback_query(call.id, text=f'Наименование: {data["new_name"]}\n'
                                                          f'Успешно сохранено!', show_alert=True)
            data['edit_user'] = data["new_name"]
            await StatesUsers.edit_user.set()
            await call.message.edit_text(f'Выбран подрядчик: {"<b>"}{data["new_name"]}{"</b>"}\n'
                                         f'Выберите поле для изменения.',
                                         parse_mode="HTML", reply_markup=KBLines.btn_change_user('CHANGE_USER'))


#########################
#    ИЗМЕНИТЬ ПАРОЛЬ
#########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['PIN_CODE'],
                                                     step_menu=['CHANGE_USER']),
                           state=[StatesUsers.edit_user])
async def change_user_pin(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    async with state.proxy() as data:
        data['edit_pin'] = CommandsDB.get_password_user_with_name_with_gp(data['edit_user'], data['user_name'])
        await StatesUsers.edit_user_pin.set()
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
                    await StatesUsers.edit_user_pin_correct.set()
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
                           state=[StatesUsers.edit_user_pin_correct])
async def save_new_pin_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if CommandsDB.update_pincode_user_with_name(data['edit_user_id'], data['new_pin']):
            await bot.answer_callback_query(call.id, text=f'PIN_CODE: {data["new_pin"]}\n'
                                                          f'Успешно сохранен!', show_alert=True)
            await StatesUsers.edit_user.set()
            await call.message.edit_text(f'Выбранный Подрядчик: {"<b>"}{data["edit_user"]}{"</b>"}\n'
                                         f'Выберите поле для изменения.',
                                         parse_mode="HTML", reply_markup=KBLines.btn_change_user('CHANGE_USER'))


###############################
# Создание нового пользователя
###############################

@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить'],
                                                     step_menu=['A_P_USERS']),
                           state=[StatesUsers.get_info_users])
async def create_new_user(call: CallbackQuery):
    await bot.answer_callback_query(call.id, cache_time=5)
    await call.message.edit_text(f'Добавление нового подрядчика\n'
                                 f'Кнопка Назад появится после ввода любого текста', reply_markup=None)
    await StatesUsers.write_user_name.set()


async def write_name_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        names_user = CommandsDB.get_all_user_with_gp(data['user_name'])
        if message.text not in names_user:
            if len(message.text) < 19:
                async with state.proxy() as data:
                    data['new_name_user'] = message.text
                await message.answer(f'Имя Ген Подрядчика: {"<b>"}{message.text}{"</b>"}\n'
                                     f'Сохранить?', parse_mode='HTML',
                                     reply_markup=KBLines.btn_next_or_back('NAME_USER'))
                await StatesUsers.user_name_correct.set()
            else:
                await message.answer(f'Длина введенного имени({"<b>"}{message.text}{"</b>"})\n'
                                     f'{len(message.text)}. Введите не более 18 символов', parse_mode="HTML")
        else:
            await message.answer(f'Подрядчик с именем({"<b>"}{message.text}{"</b>"}) уже есть в системе!\n'
                                 f'Введите другое имя, которого нету в системе.', parse_mode='HTML')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['NAME_USER']),
                           state=[StatesUsers.user_name_correct])
async def save_new_user(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pin_codes_db = CommandsDB.get_all_users(user_password=True)
        pin_code_user = random.randint(1000, 9999)
        while pin_code_user in pin_codes_db:
            pin_code_user = random.randint(1000, 9999)
        # Создаём пользователя
        if CommandsDB.add_user_with_gp(data['new_name_user'], pin_code_user, data['user_name'], data['id_user']):
            await bot.answer_callback_query(call.id,
                                            text=f'Подрядчик:{data["new_name_user"]}\n'
                                                 f'Успешно добавлен в систему!', show_alert=True)
        else:
            await bot.answer_callback_query(call.id,
                                            text=f'Не удалось добавить подрядчика: {data["new_name_user"]}'
                                                 f'в систему!', show_alert=True)
        await call.message.edit_text(f'Добро пожаловать в панель управления ГП\n'
                                     f'Вы авторизовались как {"<b>"}{data["user_name"]}{"</b>"}',
                                     parse_mode=ParseMode.HTML, reply_markup=KBLines.get_start_panel_gp())
        await StatesUsers.start_user_panel.set()


######################
#       ЗДАНИЯ
######################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Здания'],
                                                     step_menu=['USER_MAIN_PAGE']),
                           state=[StatesUsers.start_user_panel])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['BUILD', "S_BUILD"]),
                           state=[StatesUsers.build, StatesUsers.write_build])
async def get_builds(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await bot.answer_callback_query(call.id, cache_time=5)
        await StatesUsers.builds.set()
        builds = CommandsDB.get_all_builds_with_gp(data['user_name'])
        await call.message.edit_text('Для удаления здания, нажмите на его наименование',
                                     reply_markup=KBLines.get_all_builds('BUILDS', builds))


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Здание'],
                                                step_menu=['BUILDS']),
                           state=[StatesUsers.builds])
async def menu_build(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        await bot.answer_callback_query(call.id, cache_time=2)
        id_build = callback_data.get('name')
        name_build = CommandsDB.get_name_build_with_id(id_build)
        await call.message.edit_text(f'Выбрано здание: {"<b>"}{name_build}{"</b>"}',
                                     reply_markup=KBLines.btn_del_or_back('BUILD'),
                                     parse_mode="HTML")
        await StatesUsers.build.set()
        data['здание'] = name_build
        data['здание_id'] = id_build


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Удалить'],
                                                     step_menu=['BUILD']),
                           state=[StatesUsers.build])
async def del_build(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name_build = data['здание']
        build_id = data["здание_id"]
        if CommandsDB.del_name_build(build_id):
            await bot.answer_callback_query(call.id,
                                            text=f'Здание : {name_build},\n'
                                                 f'Успешно удалено.', show_alert=True)
        await StatesUsers.builds.set()
        builds = CommandsDB.get_all_builds_with_gp(data['user_name'])
        await call.message.edit_text('Для удаления здания, нажмите на его наименование и следуйте инструкции',
                                     reply_markup=KBLines.get_all_builds('BUILDS', builds))


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить'],
                                                     step_menu=['BUILDS']),
                           state=[StatesUsers.builds])
async def add_name_build(call: CallbackQuery):
    await call.message.edit_text('Введите наименование здания. Кнопка Назад появится после ввода любого текста',
                                 reply_markup=None)
    await StatesUsers.write_build.set()


async def write_name_build(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_build'] = message.text
    await message.answer(f'Наименование здания: {"<b>"}{data["name_build"]}{"</b>"}\n'
                         f'Добавить?',
                         reply_markup=KBLines.save_name('S_BUILD'), parse_mode='HTML')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить'],
                                                     step_menu=['S_BUILD']),
                           state=[StatesUsers.write_build])
async def add_name_build_in_db(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        name_build = data['name_build']
        if CommandsDB.add_name_build(name_build, data['user_name'], data['id_user']):
            await bot.answer_callback_query(call.id, text=f'Здание: {name_build}\n'
                                                          f'Успешно добавлено ', show_alert=True)
        else:
            await bot.answer_callback_query(call.id, text=f'Здание: {name_build}\n'
                                                          f'Уже есть в базе', show_alert=True)
        builds = CommandsDB.get_all_builds_with_gp(data['user_name'])
        await call.message.answer('Для удаления здания, нажмите на его наименование',
                                  reply_markup=KBLines.get_all_builds('BUILDS', builds))
        await StatesUsers.builds.set()

##########################
#     ПОСМОТРЕТЬ ФОРМЫ
##########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Посмотреть'],
                                                     step_menu=["USER_MAIN_PAGE"]),
                           state=[StatesUsers.start_user_panel])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=["SEL_FORM", "EDIT_FORM"]),
                           state=[StatesUsers.get_form_with_name, StatesUsers.edit_form])
async def get_forms_user(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    await StatesUsers.get_forms.set()
    async with state.proxy() as data:
        date = datetime.datetime.today().date()
        id_gp = data['id_user'] if data['is_GP'] else data['id_GP']
        names_forms = CommandsDB.get_name_forms_with_user_with_date(data['user_name'], date, id_gp)
        names_work = CommandsDB.get_all_names_work_with_user_id(data['id_user'])
        data_works = []
        for name_work in names_work:
            for name_form in names_forms:
                if name_form[0] == name_work[0]:
                    # contractor_id = CommandsDB.get_user_id_with_name(name_form[1], id_gp).user_id
                    contractor_id = id_gp
                    data_works.append([name_work[0], name_work[1], name_form[1], contractor_id])
        await call.message.edit_text(f"Созданные формы за {'<b>'}{date}{'</b>'}",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=KBLines.get_names_work_forms('SEE_FORM', data_works))


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Форма'],
                                                step_menu=["SEE_FORM"]),
                           state=[StatesUsers.get_forms])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=["SEL_FORM"]),
                           state=[StatesUsers.get_form_with_name])
async def change_form_user(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=3)
    await StatesUsers.edit_form.set()
    try:
        async with state.proxy() as data:
            contractor = data.get('user_name') if data.get("is_GP") else data.get('GP')
            id_contractor = data.get('id_user') if data.get("is_GP") else data.get('id_GP')
            company = data['user_name']
            company_id = data['id_user']
            is_gp = data['is_GP']
            value_from_callback_data = callback_data.get('name').split(',')
            name_work = CommandsDB.get_name_work_for_id(value_from_callback_data[0]).work_name
            ids_form = CommandsDB.get_ids_str_form_with_work_user_today(user_name=company, name_work=name_work,
                                                                        contractor=contractor)

            url = GeneratorUrlFlask.get_url_for_edit_form(company=company, work=name_work, ids=ids_form,
                                                          contractor=contractor, comp_id=company_id, gp_id=id_contractor,
                                                          is_gp=is_gp)
            await call.message.edit_text(f'[Ссылка на изменение формы]({url})',
                                         reply_markup=KBLines.btn_back('EDIT_FORM'), parse_mode="MarkdownV2")
    except Exception as e:
        print('Ошибка!', e)
        await call.message.edit_text(f'Произошла ошибка при формировании ссылки на форму. Обратитесь к Администратору',
                                     reply_markup=KBLines.btn_back('EDIT_FORM'), parse_mode="MarkdownV2")



##########################
#     СОЗДАТЬ ФОРМУ
##########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Создать форму', 'Назад'],
                                                     step_menu=["USER_MAIN_PAGE", 'ADD_NAME_WORK', "NAMES"]),
                           state=[StatesUsers.start_user_panel, StatesUsers.write_name_work,
                                  StatesUsers.select_name_work])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=["CREATE_FORM", "NEW_FORM"]),
                           state=[StatesUsers.create_form_sel_name_work, StatesUsers.get_url_form])
async def create_form(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    async with state.proxy() as data:
        await StatesUsers.create_new_form.set()
        names_work = CommandsDB.get_all_names_work_with_user_id(data['id_user'])
        await call.message.edit_text(f'Выберите наименование работ либо добавьте, чтобы продолжить:\n',
                                     reply_markup=KBLines.get_all_name_works('WRITE_FORM', names_work))


###########################################
#           НАИМЕНОВАНИЯ РАБОТ
###########################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить'],
                                                     step_menu=["WRITE_FORM"]),
                           state=[StatesUsers.create_new_form])
async def click_btn_add_name_work(call: CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Введите наименование работ, нопка Назад появится после ввода любого текста',
                                 reply_markup=None)
    await StatesUsers.write_name_work.set()


# Добавление наименования работы
async def write_name_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_work'] = message.text
    await message.answer(f'Наименование работы: {"<b>"}{data["name_work"]}{"</b>"}\n'
                         f'Добавить?',
                         reply_markup=KBLines.save_name('ADD_NAME_WORK'), parse_mode="HTML")


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить'],
                                                     step_menu=['ADD_NAME_WORK']),
                           state=[StatesUsers.write_name_work])
async def add_name_work_in_db(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        name_work = data['name_work']
        id_user = data['id_user']
        is_gp = data['is_GP']
        if CommandsDB.add_name_work(name_work, id_user, is_gp):
            await bot.answer_callback_query(call.id,
                                            text=f'Наименование работы: {name_work}\n'
                                                 f'Добавлено', show_alert=True)
        else:
            await bot.answer_callback_query(call.id,
                                            text=f'Наименование работы: {name_work}\n'
                                                 f'Уже есть в базе', show_alert=True)
        await StatesUsers.create_new_form.set()
        names_work = CommandsDB.get_all_names_work_with_user_id(data['id_user'])
        await call.message.edit_text(f'Выберите наименование работ либо добавьте, чтобы продолжить:\n',
                                     reply_markup=KBLines.get_all_name_works('WRITE_FORM', names_work))


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Работа'],
                                                step_menu=['WRITE_FORM']),
                           state=[StatesUsers.create_new_form])
async def create_form_or_del_name_work(call: CallbackQuery, state: FSMContext, callback_data: dict):
    async with state.proxy() as data:
        name_work = CommandsDB.get_name_work_for_id(callback_data.get("name")).work_name
        data['name_work'] = name_work
        data['id_work'] = callback_data.get('name')
        await call.message.edit_text(
            f'Наименование работ:\n {"<b>"}{name_work}{"</b>"}\nСоздать форму или удалить наименование работ?',
            parse_mode="HTML",
            reply_markup=KBLines.btn_create_form_or_del('CREATE_FORM'))
        await StatesUsers.create_form_sel_name_work.set()


# Удаление наименования работ
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Удалить'],
                                                     step_menu=['CREATE_FORM']),
                           state=[StatesUsers.create_form_sel_name_work])
async def del_name_work(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        id_work = data.get('id_work')
        name_work = data.get('name_work')
        if CommandsDB.del_name_work(id_work) and CommandsDB.del_str_form_with_name_work_or_id_form(name_work=name_work):
            await bot.answer_callback_query(call.id, text=f'{name_work}\n'
                                                          f'Успешно удалено! ', show_alert=True)
        else:
            await bot.answer_callback_query(call.id, text=f'{name_work}\n'
                                                          f'Удалить не удалось! ', show_alert=True)
        await StatesUsers.create_new_form.set()
        names_work = CommandsDB.get_all_names_work_with_user_id(data['id_user'])
        await call.message.edit_text(f'Выберите наименование работ либо добавьте, чтобы продолжить:\n',
                                     reply_markup=KBLines.get_all_name_works('WRITE_FORM', names_work))


# Создание формы с наименованием работ
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Создать'],
                                                     step_menu=['CREATE_FORM']),
                           state=[StatesUsers.create_form_sel_name_work])
async def create_form_with_name(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        contractor = data.get('user_name') if data.get("is_GP") else data.get('GP')
        name_work = data.get('name_work')
        company = data.get('user_name')
        id_contractor = data.get('id_user') if data.get("is_GP") else data.get('id_GP')
        is_gp = data.get('is_GP')
        comp_id = data.get('id_user')
        await StatesUsers.get_url_form.set()
        url_create_form = GeneratorUrlFlask.get_url_for_create_form(company=company, work=name_work,
                                                                    gp_id=id_contractor, contractor=contractor,
                                                                    is_gp=is_gp, comp_id=comp_id)
        await call.message.edit_text(f"{hlink('Ссылка на форму', url_create_form)}",
                                     reply_markup=KBLines.btn_back('NEW_FORM'),
                                     parse_mode=ParseMode.HTML)
        CommandsDB.change_state_reminder_chat_id(call.message.chat.id, is_remind=False)


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(write_name_work, state=StatesUsers.write_name_work)
    dp.register_message_handler(write_user_name, state=StatesUsers.edit_user_name)
    dp.register_message_handler(write_user_pin, state=StatesUsers.edit_user_pin)
    dp.register_message_handler(write_name_user, state=StatesUsers.write_user_name)
    dp.register_message_handler(write_name_build, state=StatesUsers.write_build)

