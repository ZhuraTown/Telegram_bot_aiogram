from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ParseMode
from aiogram.utils.markdown import code

from create_bot import dp, bot
from data_base.db_commands import CommandsDB
from keyboards.inlines_kb.callback_datas import menu_callback_user, btn_names_msg, workers
from keyboards.inlines_kb.kb_inlines import KBLines
from memory_FSM.bot_memory import StatesUsers, AuthorizationUser


########################
#      ГЛАВНОЕ МЕНЮ
########################

@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['AUTH_USER']),
                           state=[AuthorizationUser.correct_password_user])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад_из_формы'],
                                                     step_menu=['SEL_FORM']),
                           state=[StatesUsers.get_forms])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['WRITE_FORM']),
                           state=[StatesUsers.create_new_form])
async def cmd_users_panel(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    async with state.proxy() as data:
        await call.message.edit_text(f'Добро пожаловать в панель управления подрядчика\n'
                                     f'Вы авторизовались как {"<b>"}{data["user_name"]}{"</b>"}',
                                     parse_mode=ParseMode.HTML, reply_markup=KBLines.get_start_panel_btn())
        await StatesUsers.start_user_panel.set()


# @dp.callback_query_handler(menu_callback_user.filter(name_btn=['Главное'],
#                                                      step_menu=['Step_NAME']),
#                            state=[StatesUsers.create_new_form])
# @dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
#                                                      step_menu=['SAVE_FORM']),
#                            state=[StatesUsers.save_form])
# async def back_to_user_panel(call: CallbackQuery, state: FSMContext, callback_data: dict):
#     await call.answer(cache_time=3)
#     async with state.proxy() as data:
#         if callback_data.get('step_menu') == 'SAVE_FORM':
#
#             def get_list_user(base_dict: dict, name: str) -> list:
#                 return base_dict['workers'][name] if base_dict['workers'].get(name) else [0, 0]
#
#             user_name = data["user_name"]
#             for string_form in range(1, data.get('string') + 1):
#                 base = data.get(string_form)
#                 CommandsDB.add_new_string_work_tm(user_name=user_name, name_work=base['name_work'],
#                                                   name_stage=base['name_stage'],
#                                                   name_build=base['name_build'], level=base['level'],
#                                                   number_security=get_list_user(base, 'Охрана'),
#                                                   number_duty=get_list_user(base, 'Дежурный'),
#                                                   number_worker=get_list_user(base, 'Рабочий'),
#                                                   number_itr=get_list_user(base, 'ИТР')
#                                                   )
#
#             await bot.answer_callback_query(call.id,
#                                             text=f'Форма успешно сохранена. Её можно просмотреть в меню',
#                                             show_alert=True)
#             # # Очищаю словарь, для новых значений и корректного отображения данных
#             names_for_clean = ['name_work', 'name_stage', 'name_build',
#                                'level', 'workers', 'actual_worker', 'string']
#             for name_string in names_for_clean:
#                 del data[name_string]
#     await call.message.edit_text('Вы вернулись в меню Подрядчика', reply_markup=KBLines.get_start_panel_btn())
#     await StatesUsers.start_user_panel.set()


##########################
#     ПОСМОТРЕТЬ ФОРМЫ
##########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Посмотреть'],
                                                     step_menu=["Step_MAIN"]),
                           state=[StatesUsers.start_user_panel])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=["SEL_FORM"]),
                           state=[StatesUsers.get_form_with_name])
async def get_forms_user(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    await StatesUsers.get_forms.set()
    async with state.proxy() as data:
        names_forms = CommandsDB.get_name_forms_with_user(data['user_name'])
        msg_start = f'Созданные формы: \n'
        msg_text = ''
        msg_end = ''
        data['name_forms'] = {}
        for name, num in zip(names_forms, range(1, len(names_forms) + 1)):
            msg_text += f'{"<b>"}{num}{"</b>"} - {name}\n'
            data['name_forms'][num] = name
        await call.message.edit_text(text=msg_start + msg_text + msg_end,
                                     parse_mode=ParseMode.HTML,
                                     reply_markup=KBLines.get_names_work_forms('SEL_FORM', [i for i in range(1, len(names_forms) + 1)], names_forms))


# @dp.callback_query_handler(btn_names_msg.filter(name_btn=['Посмотреть'],
#                                                 step_menu=["SEL_FORM"]),
#                            state=[StatesUsers.get_forms])
# async def get_selected_form(call: CallbackQuery, state: FSMContext, callback_data: dict):
#     await call.answer(cache_time=3)
#     await StatesUsers.get_form_with_name.set()
#     async with state.proxy() as data:
#         name_work = data['name_forms'][int(callback_data.get("name"))]
#         strings_form = CommandsDB.get_forms_with_user_with_name(data['user_name'], name_work)
#         start_msg = "```\n"
#         end_msg = "```"
#         line_point = code(f"{'.' * 31}\n")
#         line_line = code(f"{'-' * 31}\n")
#         name_work = f'{" " * ((31 - len(name_work)) // 2)}{name_work}\n'
#         text_titles = "|  ЭТАП  |    ЗДАНИЕ    | ЭТАЖ|\n"
#         workers_title = "|Охрана|Дежурный|Рабочие| ИТР |\n"
#
#         def get_workers(d_base) -> list:
#             return [
#                 str(f"{d_base['workers']['Охрана'][0]}/{d_base['workers']['Охрана'][1]}") if d_base['workers'].get('Охрана') else ' ',
#                 str(f"{d_base['workers']['Дежурный'][0]}/{d_base['workers']['Дежурный'][1]}") if d_base['workers'].get('Дежурный') else ' ',
#                 str(f"{d_base['workers']['Рабочий'][0]}/{d_base['workers']['Рабочий'][1]}") if d_base['workers'].get('Рабочий') else ' ',
#                 str(f"{d_base['workers']['ИТР'][0]}/{d_base['workers']['ИТР'][1]}") if d_base['workers'].get('ИТР') else ' ']
#
#         table_works = start_msg + name_work + line_point
#         for strings_w in strings_form:
#             table_works += text_titles
#             table_works += f'|  {strings_w["name_stage"]:<6}| {strings_w["name_build"]:<13}| {strings_w["level"]:<4}|\n'
#             table_works += line_line + workers_title
#             workers_table = get_workers(strings_w)
#             table_works += f"| {workers_table[0]:<5}| {workers_table[1]:<7}| {workers_table[2]:<6}|{workers_table[3]:<5}|\n"
#             table_works += line_point
#         table_works += end_msg
#
#         await call.message.edit_text(text=table_works,
#                                      reply_markup=KBLines.panel_name_work('SEL_FORM'),
#                                      parse_mode=ParseMode.MARKDOWN_V2)


##########################
#     СОЗДАТЬ ФОРМУ
##########################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Создать форму', 'Назад'],
                                                     step_menu=["Step_MAIN", 'ADD_NAME_WORK', "NAMES"]),
                           state=[StatesUsers.start_user_panel, StatesUsers.write_name_work,
                                  StatesUsers.select_name_work])
async def create_form(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=3)
    async with state.proxy() as data:
        await StatesUsers.create_new_form.set()
        link = CommandsDB.get_link('google_form')
        await call.message.edit_text(f'Перейдите по ссылке и заполните форму в GoogleForms:\n'
                                     f'{link}',
                                     reply_markup=KBLines.btn_back('WRITE_FORM'))


###########################################
#           НАИМЕНОВАНИЯ РАБОТ
###########################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить имя']),
                           state=[StatesUsers.create_new_form])
async def click_btn_add_name_work(call: CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text('Введите наименование работ', reply_markup=None)
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
        if CommandsDB.add_name_work(name_work):
            await bot.answer_callback_query(call.id,
                                            text=f'Наименование работы: {name_work}\n'
                                                 f'Добавлено', show_alert=True)
        else:
            await bot.answer_callback_query(call.id,
                                            text=f'Наименование работы: {name_work}\n'
                                                 f'Уже есть в базе', show_alert=True)
    await call.message.answer('Заполнение формы\nВыберите следующий шаг',
                              reply_markup=KBLines.step_name_work())
    await StatesUsers.create_new_form.set()


##############################################################################################
#                            ВЫБРАТЬ    НАИМЕНОВАНИЕ        РАБОТ
##############################################################################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Посмотреть', 'Назад'],
                                                     step_menu=['Step_NAME', "SEL_NAME", 'STAGE']),
                           state=[StatesUsers.create_new_form, StatesUsers.step_stage_work,
                                  StatesUsers.select_name_work])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['DEL_NAMES']),
                           state=[StatesUsers.select_name_work])
async def step_select_name_work(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    names_work_db = CommandsDB.get_all_names_work() if len(CommandsDB.get_all_names_work()) > 0 else False
    if names_work_db:
        await call.message.answer(f'Выберите наименование работ\n и нажмите кнопку Продолжить\n',
                                  reply_markup=KBLines.get_names_work_one_msg("NAMES", names_work_db),
                                  parse_mode="HTML")
        await StatesUsers.select_name_work.set()
    else:
        await call.message.answer('Наименований работ нет.\n'
                                  'Добавьте наименование работ, чтобы продолжить',
                                  reply_markup=KBLines.btn_back('NAMES'))
        await StatesUsers.select_name_work.set()


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Удалить'],
                                                step_menu=['NAMES']),
                           state=[StatesUsers.select_name_work])
async def delete_name_work(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        name_work = CommandsDB.get_name_work_for_id(callback_data.get('name'))
        data['id_name_work_del'] = callback_data.get('name')
        data['name_work_del'] = name_work
        await call.message.edit_text(f'Наименование работ: {"<b>"}{name_work}{"</b>"}.\n'
                                     f'Удалить?',
                                     reply_markup=KBLines.btn_del_or_back('DEL_NAMES'), parse_mode="HTML")


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Удалить'],
                                                     step_menu=['DEL_NAMES']),
                           state=[StatesUsers.select_name_work])
async def accept_del_name_work(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        name_work_id = data['id_name_work_del']
        name_work = data['name_work_del']
        if CommandsDB.del_name_work(name_work_id):
            await bot.answer_callback_query(call.id,
                                            text=f'Наименование работы:{name_work},\n'
                                                 f'Успешно удалено.', show_alert=True)
            del data['name_work_del']
            del data['id_name_work_del']
            names_work_db = CommandsDB.get_all_names_work() if len(CommandsDB.get_all_names_work()) > 0 else False
            if names_work_db:
                await call.message.answer(f'Выберите наименование работ\n и нажмите кнопку Продолжить\n',
                                          reply_markup=KBLines.get_names_work_one_msg("NAMES", names_work_db),
                                          parse_mode="HTML")
                await StatesUsers.select_name_work.set()
            else:
                await call.message.edit_text('Наименований работ нет.\n'
                                             'Добавьте наименование работ, чтобы продолжить',
                                             reply_markup=KBLines.btn_back('NAMES'))
                await StatesUsers.select_name_work.set()
        else:
            await bot.answer_callback_query(call.id,
                                            text=f'Наименование работы:{name_work},\n'
                                                 f'Удалить не удалось.', show_alert=True)
            await StatesUsers.select_name_work.set()


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['select', 'Имя'],
                                                step_menu=['NAMES']),
                           state=[StatesUsers.select_name_work])
async def select_name_work(call: CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get('name_btn') == 'Имя':
        await call.answer(cache_time=1)
    else:
        async with state.proxy() as data:
            name_work = CommandsDB.get_name_work_for_id(callback_data.get('name'))
            data['name_work'] = name_work
        await call.message.edit_text(f'Наименование работы:{"<b>"}{name_work}{"</b>"}\n'
                                     f'Успешно выбрано', reply_markup=KBLines.btn_next_or_back('SEL_NAME'),
                                     parse_mode="HTML")
        await StatesUsers.step_stage_work.set()


################################################
#                   ЭТАПЫ
################################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['ADD_S_FORM']),
                           state=[StatesUsers.add_string], )
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['SEL_NAME']),
                           state=[StatesUsers.step_stage_work, StatesUsers.write_stage_work], )
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['W_STAGE', 'BUILD']),
                           state=[StatesUsers.step_stage_work, StatesUsers.write_stage_work,
                                  StatesUsers.step_build_work], )
async def step_stage(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await StatesUsers.step_stage_work.set()
    async with state.proxy() as data:
        name_work = data['name_work']
        if callback_data.get('step_menu') == "ADD_S_FORM":
            # Очищаю словарь, от старых данных
            names_for_clean = ['name_stage', 'name_build', 'level', 'workers', 'actual_worker']
            for name_string in names_for_clean:
                del data[name_string]
            await call.message.edit_text(f'{"<b>"}{name_work}{"</b>"}\n'
                                         f'--------------------------------\n'
                                         f'Введите этап работы для новой строки.',
                                         reply_markup=KBLines.get_kb_stage('STAGE'), parse_mode='HTML')
        else:
            await call.message.edit_text(f'{"<b>"}{name_work}{"</b>"}\n'
                                         f'--------------------------------\n'
                                         f'Введите этап работы.',
                                         reply_markup=KBLines.get_kb_stage('STAGE'), parse_mode='HTML')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Ввести этап'],
                                                     step_menu=['STAGE']),
                           state=[StatesUsers.step_build_work, StatesUsers.step_stage_work])
async def step_write_stage_work(call: CallbackQuery):
    await call.message.edit_text('Введите этап работы', reply_markup=None)
    await StatesUsers.write_stage_work.set()


async def write_stage_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_stage'] = message.text
    await message.answer(f"Введенный этап работы: {'<b>'}{data['name_stage']}{'</b>'} \n"
                         f"Продолжить?", reply_markup=KBLines.btn_next_or_back('W_STAGE'), parse_mode="HTML")


###################################
#             ЗДАНИЯ
###################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить', ],
                                                     step_menu=['W_STAGE']),
                           state=[StatesUsers.write_stage_work])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад', ],
                                                     step_menu=['S_BUILD', 'BUILDS']),
                           state=[StatesUsers.write_build_work, StatesUsers.select_build_work])
async def step_build(call: CallbackQuery, state: FSMContext):
    await StatesUsers.step_build_work.set()
    async with state.proxy() as data:
        await call.message.edit_text(f'{"<b>"}{data["name_work"]}{"</b>"}\n'
                                     f'|Этап: {"<b>"}{data["name_stage"]}{"</b>"}\n'
                                     f'--------------------------------\n'
                                     f'Выберите следующий шаг.',
                                     reply_markup=KBLines.step_build_work('BUILD'), parse_mode='HTML')


# Ввести наименование здание
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить здание'],
                                                     step_menu=['BUILD']),
                           state=[StatesUsers.step_build_work])
async def add_name_build(call: CallbackQuery):
    await call.message.edit_text('Введите наименование здания', reply_markup=None)
    await StatesUsers.write_build_work.set()


async def write_name_build(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_build'] = message.text
    await message.answer(f'Наименование здания: {"<b>"}{data["name_build"]}{"</b>"}\n'
                         f'Добавить?',
                         reply_markup=KBLines.save_name('S_BUILD'), parse_mode='HTML')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить'],
                                                     step_menu=['S_BUILD']),
                           state=[StatesUsers.write_build_work])
async def add_name_build_in_db(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        name_build = data['name_build']
        if CommandsDB.add_name_build(name_build):
            await bot.answer_callback_query(call.id, text=f'Здание: {name_build}\n'
                                                          f'Успешно добавлено ', show_alert=True)
        else:
            await bot.answer_callback_query(call.id, text=f'Здание: {name_build}\n'
                                                          f'Уже есть в базе', show_alert=True)
    await call.message.answer(f'{"<b>"}{data["name_work"]}{"</b>"}\n'
                              f'|Этап: {"<b>"}{data["name_stage"]}{"</b>"}\n'
                              f'--------------------------------\n'
                              f'Выберите следующий шаг.',
                              reply_markup=KBLines.step_build_work('BUILD'), parse_mode='HTML')
    await StatesUsers.step_build_work.set()


######################################################################
#                               ВЫБОР ЗДАНИЯ
######################################################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Посмотреть здания', 'Назад'],
                                                     step_menu=['BUILD', 'SEL_BUILD', 'LEVEL']),
                           state=[StatesUsers.step_build_work, StatesUsers.write_level_build_work,
                                  StatesUsers.step_level_build_work])
async def select_build_work(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    builds_work_db = CommandsDB.get_all_names_builds() if len(CommandsDB.get_all_names_builds()) > 0 else False
    if builds_work_db:
        await call.message.answer(f'Выберите здание\n и нажмите кнопку Продолжить',
                                  reply_markup=KBLines.get_names_one_msg("BUILDS", builds_work_db))
        await StatesUsers.select_build_work.set()
    else:
        await call.message.answer('Зданий нет.\n'
                                  'Добавьте здание, чтобы продолжить',
                                  reply_markup=KBLines.btn_back('BUILDS'))
        await StatesUsers.select_build_work.set()


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Удалить'],
                                                step_menu=['BUILDS']),
                           state=[StatesUsers.select_build_work])
async def delete_build_work(call: CallbackQuery, callback_data: dict):
    name_build = callback_data.get('name')
    if CommandsDB.del_name_build(name_build):
        await bot.answer_callback_query(call.id,
                                        text=f'Здание : {name_build},\n'
                                             f'Успешно удалено.', show_alert=True)
        builds_work_db = [name[1] for name in CommandsDB.get_all_names_builds()] if len(
            CommandsDB.get_all_names_builds()) > 0 else False

        if builds_work_db:
            await call.message.edit_text(f'Выберите здание\n и нажмите кнопку Продолжить',
                                         reply_markup=KBLines.get_names_one_msg("BUILDS", builds_work_db))
            await StatesUsers.select_build_work.set()
        else:
            await call.message.edit_text('Зданий нет.\n'
                                         'Добавьте здание, чтобы продолжить',
                                         reply_markup=KBLines.btn_back('BUILDS'))
            await StatesUsers.select_build_work.set()
    else:
        await bot.answer_callback_query(call.id,
                                        text=f'Здание:{name_build},\n'
                                             f'Удалить не удалось.', show_alert=True)
        await StatesUsers.select_build_work.set()


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['select', 'Имя'],
                                                step_menu=['BUILDS']),
                           state=[StatesUsers.select_build_work])
async def select_name_work(call: CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get('name_btn') == 'Имя':
        await call.answer(cache_time=1)
    else:
        async with state.proxy() as data:
            data['name_build'] = CommandsDB.get_name_build_with_id(callback_data.get('name'))
        name_build = CommandsDB.get_name_build_with_id(callback_data.get('name'))
        await call.message.edit_text(f'Здание : {"<b>"}{name_build}{"</b>"}\n'
                                     f'Успешно выбрано', reply_markup=KBLines.btn_next_or_back('SEL_BUILD'),
                                     parse_mode="HTML")
        await StatesUsers.step_level_build_work.set()


##################################################
#                  ЭТАЖИ
##################################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['SEL_BUILD']),
                           state=[StatesUsers.step_level_build_work, ], )
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['W_LEVEL', 'WORKERS']),
                           state=[StatesUsers.write_level_build_work, StatesUsers.step_workers], )
async def step_build(call: CallbackQuery, state: FSMContext):
    await StatesUsers.step_level_build_work.set()
    async with state.proxy() as data:
        await call.message.edit_text(f'{"<b>"}{data["name_work"]}{"</b>"}\n'
                                     f'|Этап: {"<b>"}{data["name_stage"]}{"</b>"}\n'
                                     f'|Здание: {"<b>"}{data["name_build"]}{"</b>"}\n'
                                     f'--------------------------------\n'
                                     f'Выберите следующий шаг.',
                                     reply_markup=KBLines.get_kb_level('LEVEL'), parse_mode='HTML')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Ввести этаж'],
                                                     step_menu=['LEVEL']),
                           state=[StatesUsers.step_level_build_work, StatesUsers.step_stage_work])
async def step_write_build_work(call: CallbackQuery):
    await call.message.edit_text('Введите этаж', reply_markup=None)
    await StatesUsers.write_level_build_work.set()


async def write_level_build_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['level'] = message.text
    await message.answer(f"Введенный этаж: {'<b>'}{data['level']}{'</b>'} \n"
                         f"Продолжить?", reply_markup=KBLines.btn_next_or_back('W_LEVEL'), parse_mode="HTML")


##############################################
#             ВЫБОР СОТРУДНИКОВ
#############################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить', ],
                                                     step_menu=['W_LEVEL', ]),
                           state=[StatesUsers.write_level_build_work, ], )
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад', 'Добавить'],
                                                     step_menu=['SEL_WORKER', 'F_WORKERS']),
                           state=[StatesUsers.select_plan_workers, StatesUsers.finish_write_workers], )
async def step_workers(call: CallbackQuery, state: FSMContext):
    await StatesUsers.step_workers.set()
    async with state.proxy() as data:
        if "workers" not in data:
            data['workers'] = {}

        text_msg = f'{"<b>"}{data["name_work"]}{"</b>"}\n' \
                   f'|Этап: {"<b>"}{data["name_stage"]}{"</b>"}\n' \
                   f'|Здание: {"<b>"}{data["name_build"]}{"</b>"}\n' \
                   f'|Этаж: {"<b>"}{data["level"]}{"</b>"}\n' \
                   f'--------------------------------\n'

        text_end = 'Выберите следующий шаг.'
        if len(data['workers']) == 0:
            await call.message.edit_text(text=text_msg + text_end,
                                         reply_markup=KBLines.get_kb_workers('WORKERS'), parse_mode='HTML')
        else:
            text_msg = text_msg + 'Сотрудники (План/Факт) \n' \
                                  '--------------------------------\n'
            for worker, count in data['workers'].items():
                text_msg = text_msg + f'{"<b>"}{worker} : ({count[0]}/{0 if count[1] is None else count[1]}{"</b>"})\n'
            await call.message.edit_text(text=text_msg + text_end,
                                         reply_markup=KBLines.get_kb_workers('WORKERS'), parse_mode='HTML')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Сотрудник', 'Назад'],
                                                     step_menu=['WORKERS', 'PLAN_WORKERS']),
                           state=[StatesUsers.step_workers, StatesUsers.select_plan_workers,
                                  StatesUsers.write_actually_workers])
async def select_worker_plan(call: CallbackQuery):
    await StatesUsers.select_plan_workers.set()
    await call.message.edit_text(f'Выберите сотрудника для заполнения\n'
                                 f'и нажмите кнопку Продолжить',
                                 reply_markup=KBLines.get_workers_menu('SEL_WORKER'))


@dp.callback_query_handler(workers.filter(name_btn=['Выбрать', 'Имя'],
                                          step_menu=['SEL_WORKER']),
                           state=[StatesUsers.select_plan_workers, StatesUsers.write_plan_workers, ], )
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['W_ACTUAL_WORKERS', 'W_PLAN_WORKERS']),
                           state=[StatesUsers.finish_write_workers, StatesUsers.write_actually_workers], )
async def select_worker_for_plan(call: CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get('name_btn') == 'Имя':
        await call.answer(cache_time=1)
    elif callback_data.get('name_btn') == 'Выбрать':
        async with state.proxy() as data:
            selected_worker = callback_data.get('name')
            data['actual_worker'] = selected_worker
            await call.message.edit_text(f'Выбран сотрудник: {"<b>"}{selected_worker}{"</b>"}',
                                         reply_markup=KBLines.btn_next_or_back('PLAN_WORKERS'),
                                         parse_mode='HTML')
    elif callback_data.get('name_btn') == 'Назад':
        async with state.proxy() as data:
            await call.message.edit_text(f'Выбран сотрудник: {"<b>"}{data["actual_worker"]}{"</b>"}',
                                         reply_markup=KBLines.btn_next_or_back('PLAN_WORKERS'),
                                         parse_mode='HTML')
            await StatesUsers.select_plan_workers.set()


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['PLAN_WORKERS']),
                           state=[StatesUsers.select_plan_workers], )
async def select_write_worker_plan(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await StatesUsers.write_plan_workers.set()
        await call.message.edit_text(f'Выбран сотрудник: {"<b>"}{data["actual_worker"]}{"</b>"}\n'
                                     f'Введите планируемое количество сотрудников',
                                     reply_markup=None,
                                     parse_mode='HTML')


async def write_worker_plan(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            if data['actual_worker'] not in data['workers']:
                data['workers'][data['actual_worker']] = [None, None]
            data['workers'][data['actual_worker']][0] = message.text
        await message.answer(f"Тип сотрудник: {'<b>'}{data['actual_worker']}{'</b>'} \n"
                             f"План: {'<b>'}{data['workers'][data['actual_worker']][0]}{'</b>'} \n"
                             f"Продолжить?", reply_markup=KBLines.btn_next_or_back('W_PLAN_WORKERS'),
                             parse_mode="HTML")
        await StatesUsers.write_actually_workers.set()
    else:
        await message.answer(f"Нужно ввести только число \n"
                             f"{message.text} не число!")


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['W_PLAN_WORKERS']),
                           state=[StatesUsers.write_actually_workers], )
async def select_write_worker_actually(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.edit_text(f'Выбран сотрудник: {"<b>"}{data["actual_worker"]}{"</b>"}\n'
                                     f'План: {"<b>"}{data["workers"][data["actual_worker"]][0]}{"</b>"}\n'
                                     f'Введите фактическое количество сотрудников',
                                     reply_markup=None,
                                     parse_mode='HTML')


async def write_worker_actually(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['workers'][data['actual_worker']][1] = message.text
        await message.answer(f"Тип сотрудник: {'<b>'}{data['actual_worker']}{'</b>'} \n"
                             f"План: {'<b>'}{data['workers'][data['actual_worker']][0]}{'</b>'}\n"
                             f"Факт: {'<b>'}{data['workers'][data['actual_worker']][1]}{'</b>'}\n"
                             f"Продолжить?", reply_markup=KBLines.btn_next_or_back('W_ACTUAL_WORKERS'),
                             parse_mode="HTML")
        await StatesUsers.finish_write_workers.set()
    else:
        await message.answer(f"Нужно ввести только число \n"
                             f"{message.text} не число!")


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить', 'Назад'],
                                                     step_menu=['W_ACTUAL_WORKERS', 'S_A_FORM']),
                           state=[StatesUsers.finish_write_workers, StatesUsers.step_save_or_add_string], )
async def select_write_worker_actually(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text_msg = 'Сотрудники (План/Факт) \n' \
                   '------------------------\n'
        text_msg_end = 'Добавить еще сотрудников?'
        # Если пользователь ввёл план кол-во сотрудников, но не стал вводить фактическое,
        # То пользователь будет висеть в словаре с None вместо фактического кол-во сотрудников
        worker_for_del = []
        for worker, count in data['workers'].items():
            if not count[1]:
                worker_for_del.append(worker)
        for name_worker in worker_for_del:
            del data['workers'][name_worker]

        for worker, count in data['workers'].items():
            text_msg = text_msg + f'{"<b>"}{worker} : ({count[0]}/{count[1]}{"</b>"})\n'
        await call.message.edit_text(text=text_msg + text_msg_end,
                                     reply_markup=KBLines.add_new_worker('F_WORKERS'),
                                     parse_mode='HTML')
        await StatesUsers.finish_write_workers.set()


########################################
#   СОХРАНИТЬ ФОРМУ/ ДОБАВИТЬ СТРОКУ
########################################

@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить', "Назад"],
                                                     step_menu=['F_WORKERS', ]),
                           state=[StatesUsers.finish_write_workers, StatesUsers.save_form])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=["Назад"],
                                                     step_menu=['SAVE_FORM', 'ADD_S_FORM']),
                           state=[StatesUsers.save_form, StatesUsers.add_string])
async def save_or_add_string(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await StatesUsers.step_save_or_add_string.set()
    async with state.proxy() as data:
        if callback_data.get('name_btn') == 'Продолжить':
            if not data.get('string'):
                data['string'] = 1
                data[data['string']] = dict()
                keys_list = ['name_stage', 'name_work', 'name_build', 'level', 'workers', 'user_name']
                for key in keys_list:
                    data[data['string']][key] = data.get(key)
            else:
                data['string'] = data['string'] + 1
                data[data['string']] = dict()
                keys_list = ['name_stage', 'name_work', 'name_build', 'level', 'workers', 'user_name']
                for key in keys_list:
                    data[data['string']][key] = data.get(key)
        # Оформление сообщения
        start_msg = "```\n"
        end_msg = "```"
        line_point = code(f"{'.' * 31}\n")
        line_line = code(f"{'-' * 31}\n")
        name_work = f'{" " * ((31 - len(data["name_work"])) // 2)}{data["name_work"]}\n'
        text_titles = "|  ЭТАП  |    ЗДАНИЕ    | ЭТАЖ|\n"
        workers_title = "|Охрана|Дежурный|Рабочие| ИТР |\n"

        def get_workers(d_base) -> list:
            return [
                str(d_base['workers']['Охрана'][0] + '/' + d_base['workers']['Охрана'][1]) if d_base['workers'].get('Охрана') else ' ',
                str(d_base['workers']['Дежурный'][0] + '/' + d_base['workers']['Дежурный'][1]) if d_base['workers'].get('Дежурный') else ' ',
                str(d_base['workers']['Рабочий'][0] + '/' + d_base['workers']['Рабочий'][1]) if d_base['workers'].get('Рабочий') else ' ',
                str(d_base['workers']['ИТР'][0] + '/' + d_base['workers']['ИТР'][1]) if d_base['workers'].get('ИТР') else ' ']

        table_works = start_msg + name_work + line_point
        for string_w in range(1, data.get('string') + 1):
            base = data.get(string_w)
            table_works += text_titles
            table_works += f'|  {base["name_stage"]:<6}| {base["name_build"]:<13}| {base["level"]:<4}|\n'
            table_works += line_line + workers_title
            workers_table = get_workers(base)
            table_works += f"| {workers_table[0]:<5}| {workers_table[1]:<7}| {workers_table[2]:<6}|{workers_table[3]:<5}|\n"
            table_works += line_point
        table_works += end_msg
        await call.message.edit_text(text=table_works,
                                     reply_markup=KBLines.save_or_add_string('S_A_FORM'),
                                     parse_mode=ParseMode.MARKDOWN_V2)


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Сохранить', ],
                                                     step_menu=['S_A_FORM']),
                           state=[StatesUsers.step_save_or_add_string])
async def save_form(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await StatesUsers.save_form.set()
        await call.message.edit_text(text='Сохранить форму?',
                                     reply_markup=KBLines.btn_next_or_back('SAVE_FORM'), parse_mode='HTML')


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить', ],
                                                     step_menu=['S_A_FORM']),
                           state=[StatesUsers.step_save_or_add_string])
async def save_form(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await StatesUsers.add_string.set()
        await call.message.edit_text(text='Добавить строчку в форму?',
                                     reply_markup=KBLines.btn_next_or_back('ADD_S_FORM'), parse_mode='HTML')


def register_handlers_users(dp: Dispatcher):
    dp.register_message_handler(write_name_work, state=StatesUsers.write_name_work)
    dp.register_message_handler(write_stage_work, state=StatesUsers.write_stage_work)
    dp.register_message_handler(write_level_build_work, state=StatesUsers.write_level_build_work)
    dp.register_message_handler(write_name_build, state=StatesUsers.write_build_work)
    dp.register_message_handler(write_worker_plan, state=StatesUsers.write_plan_workers)
    dp.register_message_handler(write_worker_actually, state=StatesUsers.write_actually_workers)
