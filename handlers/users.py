import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ParseMode

from create_bot import dp, bot
from data_base.db_commands import CommandsDB
from keyboards.inlines_kb.callback_datas import menu_callback_user, btn_names_msg
from keyboards.inlines_kb.kb_inlines import KBLines
from memory_FSM.bot_memory import StatesUsers, AuthorizationUser
from flask_server.generator_url import GeneratorUrlFlask


########################
#      ГЛАВНОЕ МЕНЮ
########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['AUTH_USER']),
                           state=[AuthorizationUser.correct_password_user])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['WRITE_FORM', "SEE_FORM"]),
                           state=[StatesUsers.create_new_form, StatesUsers.get_forms])
async def cmd_users_panel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    async with state.proxy() as data:
        await call.message.edit_text(f'Добро пожаловать в панель управления подрядчика\n'
                                     f'Вы авторизовались как {"<b>"}{data["user_name"]}{"</b>"}',
                                     parse_mode=ParseMode.HTML, reply_markup=KBLines.get_start_panel_btn())
        await StatesUsers.start_user_panel.set()


##########################
#     ПОСМОТРЕТЬ ФОРМЫ
##########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Посмотреть'],
                                                     step_menu=["Step_MAIN"]),
                           state=[StatesUsers.start_user_panel])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=["SEL_FORM", "EDIT_FORM"]),
                           state=[StatesUsers.get_form_with_name, StatesUsers.edit_form])
async def get_forms_user(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    await StatesUsers.get_forms.set()
    async with state.proxy() as data:
        works_with_ids = {}
        date = datetime.datetime.today().date()
        names_forms = CommandsDB.get_name_forms_with_user_with_date(data['user_name'], date)
        names_work = CommandsDB.get_all_names_work_with_user_id(data['id_user'])
        for name_work in names_work:
            for name_form in names_forms:
                if name_form == name_work[0]:
                    works_with_ids[name_work[0]] = name_work[1]
        await call.message.edit_text(f"Созданные формы за {'<b>'}{date}{'</b>'}",
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=KBLines.get_names_work_forms('SEE_FORM', works_with_ids))


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Форма'],
                                                step_menu=["SEE_FORM"]),
                           state=[StatesUsers.get_forms])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=["SEL_FORM"]),
                           state=[StatesUsers.get_form_with_name])
async def get_forms_user(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer(cache_time=3)
    await StatesUsers.edit_form.set()
    async with state.proxy() as data:
        company = data['user_name']
        name_work = CommandsDB.get_name_work_for_id(callback_data.get('name'))
        ids_form = CommandsDB.get_ids_str_form_with_work_user_today(user_name=company, name_work=name_work)
        url = GeneratorUrlFlask.get_url_for_edit_form(company=company, work=name_work, ids=ids_form)
        await call.message.edit_text(f'Ссылка на изменение формы:\n {url}', reply_markup=KBLines.btn_del_or_back('EDIT_FORM'))


##########################
#     СОЗДАТЬ ФОРМУ
##########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Создать форму', 'Назад'],
                                                     step_menu=["Step_MAIN", 'ADD_NAME_WORK', "NAMES"]),
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
        if CommandsDB.add_name_work(name_work, id_user):
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
        name_work = CommandsDB.get_name_work_for_id(callback_data.get("name"))
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
        name_work = data.get('name_work')
        company = data.get('user_name')
        await StatesUsers.get_url_form.set()
        url_create_form = GeneratorUrlFlask.get_url_for_create_form(company=company, work=name_work)
        await call.message.edit_text(f"Ссылка на форму:\n"
                                     f"{url_create_form}", reply_markup=KBLines.btn_back('NEW_FORM'))


# ##############################################################################################
# #                            ВЫБРАТЬ    НАИМЕНОВАНИЕ        РАБОТ
# ##############################################################################################
# @dp.callback_query_handler(menu_callback_user.filter(name_btn=['Посмотреть', 'Назад'],
#                                                      step_menu=['Step_NAME', "SEL_NAME", 'STAGE']),
#                            state=[StatesUsers.create_new_form, StatesUsers.step_stage_work,
#                                   StatesUsers.select_name_work])
# @dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
#                                                      step_menu=['DEL_NAMES']),
#                            state=[StatesUsers.select_name_work])
# async def step_select_name_work(call: CallbackQuery):
#     await call.message.edit_reply_markup(reply_markup=None)
#     names_work_db = CommandsDB.get_all_names_work() if len(CommandsDB.get_all_names_work()) > 0 else False
#     if names_work_db:
#         await call.message.answer(f'Выберите наименование работ\n и нажмите кнопку Продолжить\n',
#                                   reply_markup=KBLines.get_names_work_one_msg("NAMES", names_work_db),
#                                   parse_mode="HTML")
#         await StatesUsers.select_name_work.set()
#     else:
#         await call.message.answer('Наименований работ нет.\n'
#                                   'Добавьте наименование работ, чтобы продолжить',
#                                   reply_markup=KBLines.btn_back('NAMES'))
#         await StatesUsers.select_name_work.set()
#
#
# @dp.callback_query_handler(btn_names_msg.filter(name_btn=['Удалить'],
#                                                 step_menu=['NAMES']),
#                            state=[StatesUsers.select_name_work])
# async def delete_name_work(call: CallbackQuery, callback_data: dict, state: FSMContext):
#     async with state.proxy() as data:
#         name_work = CommandsDB.get_name_work_for_id(callback_data.get('name'))
#         data['id_name_work_del'] = callback_data.get('name')
#         data['name_work_del'] = name_work
#         await call.message.edit_text(f'Наименование работ: {"<b>"}{name_work}{"</b>"}.\n'
#                                      f'Удалить?',
#                                      reply_markup=KBLines.btn_del_or_back('DEL_NAMES'), parse_mode="HTML")
#
#
# @dp.callback_query_handler(menu_callback_user.filter(name_btn=['Удалить'],
#                                                      step_menu=['DEL_NAMES']),
#                            state=[StatesUsers.select_name_work])
# async def accept_del_name_work(call: CallbackQuery, callback_data: dict, state: FSMContext):
#     async with state.proxy() as data:
#         name_work_id = data['id_name_work_del']
#         name_work = data['name_work_del']
#         if CommandsDB.del_name_work(name_work_id):
#             await bot.answer_callback_query(call.id,
#                                             text=f'Наименование работы:{name_work},\n'
#                                                  f'Успешно удалено.', show_alert=True)
#             del data['name_work_del']
#             del data['id_name_work_del']
#             names_work_db = CommandsDB.get_all_names_work() if len(CommandsDB.get_all_names_work()) > 0 else False
#             if names_work_db:
#                 await call.message.answer(f'Выберите наименование работ\n и нажмите кнопку Продолжить\n',
#                                           reply_markup=KBLines.get_names_work_one_msg("NAMES", names_work_db),
#                                           parse_mode="HTML")
#                 await StatesUsers.select_name_work.set()
#             else:
#                 await call.message.edit_text('Наименований работ нет.\n'
#                                              'Добавьте наименование работ, чтобы продолжить',
#                                              reply_markup=KBLines.btn_back('NAMES'))
#                 await StatesUsers.select_name_work.set()
#         else:
#             await bot.answer_callback_query(call.id,
#                                             text=f'Наименование работы:{name_work},\n'
#                                                  f'Удалить не удалось.', show_alert=True)
#             await StatesUsers.select_name_work.set()
#
#
# @dp.callback_query_handler(btn_names_msg.filter(name_btn=['select', 'Имя'],
#                                                 step_menu=['NAMES']),
#                            state=[StatesUsers.select_name_work])
# async def select_name_work(call: CallbackQuery, callback_data: dict, state: FSMContext):
#     if callback_data.get('name_btn') == 'Имя':
#         await call.answer(cache_time=1)
#     else:
#         async with state.proxy() as data:
#             name_work = CommandsDB.get_name_work_for_id(callback_data.get('name'))
#             data['name_work'] = name_work
#         await call.message.edit_text(f'Наименование работы:{"<b>"}{name_work}{"</b>"}\n'
#                                      f'Успешно выбрано', reply_markup=KBLines.btn_next_or_back('SEL_NAME'),
#                                      parse_mode="HTML")
#         await StatesUsers.step_stage_work.set()


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(write_name_work, state=StatesUsers.write_name_work)
    # dp.register_message_handler(write_stage_work, state=StatesUsers.write_stage_work)
    # dp.register_message_handler(write_level_build_work, state=StatesUsers.write_level_build_work)
    # dp.register_message_handler(write_name_build, state=StatesUsers.write_build_work)
    # dp.register_message_handler(write_worker_plan, state=StatesUsers.write_plan_workers)
    # dp.register_message_handler(write_worker_actually, state=StatesUsers.write_actually_workers)
