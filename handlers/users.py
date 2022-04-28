from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from create_bot import dp, bot
from data_base.db_commands import CommandsDB
from keyboards.classic_kb import kb_btn_back
from keyboards.inlines_kb.callback_datas import workers_callback, menu_callback, add_users, menu_callback_user, \
    btn_names_msg, workers
from keyboards.inlines_kb.kb_inlines import KBLines, get_inline_workers_panel, get_panel_attempt_add_users, \
    get_btn_add_users, save_form_or_add_string
from memory_FSM.bot_memory import StatesUsers


########################
#      ГЛАВНОЕ МЕНЮ
########################
async def cmd_users_panel(message: types.Message):
    await message.delete()
    await message.answer('Панель управления Подрядчика', reply_markup=KBLines.get_start_panel_btn())
    await StatesUsers.start_user_pamel.set()


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Главное'],
                                                     step_menu=['Step_NAME']),
                           state=[StatesUsers.create_new_form])
async def back_to_user_panel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Вы вернулись в меню Подрядчика', reply_markup=KBLines.get_start_panel_btn())
    await state.reset_state()
    await StatesUsers.start_user_pamel.set()


##########################
#     СОЗДАТЬ ФОРМУ
##########################

@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Создать форму', 'Назад'],
                                                     step_menu=["Step_MAIN", 'ADD_NAME_WORK', "NAMES"]),
                           state=[StatesUsers.start_user_pamel, StatesUsers.write_name_work,
                                  StatesUsers.select_name_work])
async def create_form(call: CallbackQuery):
    await StatesUsers.create_new_form.set()
    await call.message.edit_text('Заполнение формы \n Выберите следующий шаг',
                                 reply_markup=KBLines.step_name_work())


###########################################
#           НАИМЕНОВАНИЯ РАБОТ
###########################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Добавить имя']),
                           state=[StatesUsers.create_new_form])
async def click_btn_add_name_work(call: CallbackQuery):
    await call.message.edit_text('Введите наименование работ', reply_markup=None)
    await StatesUsers.write_name_work.set()


# Добавление наименования работы
async def write_name_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_work'] = message.text
    await message.answer(f'Наименование работы: {data["name_work"]}\n'
                         f'Добавить?',
                         reply_markup=KBLines.save_name('ADD_NAME_WORK'))


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
    await call.message.answer('Заполнение формы \n Выберите следующий шаг',
                              reply_markup=KBLines.step_name_work())
    await StatesUsers.create_new_form.set()


##############################################################################################
#                            ВЫБРАТЬ    НАИМЕНОВАНИЕ        РАБОТ
##############################################################################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Посмотреть', 'Назад'],
                                                     step_menu=['Step_NAME', "SEL_NAME", 'STAGE']),
                           state=[StatesUsers.create_new_form, StatesUsers.step_stage_work,
                                  StatesUsers.select_name_work])
async def step_select_name_work(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    names_work_db = [name[1] for name in CommandsDB.get_all_names_work()] if len(
        CommandsDB.get_all_names_work()) > 0 else False
    if names_work_db:
        await call.message.answer(f'Выберите наименование работ\n и нажмите кнопку Продолжить',
                                  reply_markup=KBLines.get_names_one_msg("NAMES", names_work_db))
        await StatesUsers.select_name_work.set()
    else:
        await call.message.answer('Наименований работ нет.\n'
                                  'Добавьте наименование работ, чтобы продолжить',
                                  reply_markup=KBLines.btn_back('NAMES'))
        await StatesUsers.select_name_work.set()


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Удалить'],
                                                step_menu=['NAMES']),
                           state=[StatesUsers.select_name_work])
async def delete_name_work(call: CallbackQuery, callback_data: dict):
    name_work = callback_data.get('name')
    if CommandsDB.del_name_work(name_work):
        await bot.answer_callback_query(call.id,
                                        text=f'Наименование работы:{name_work},\n'
                                             f'Успешно удалено.', show_alert=True)

        names_work_db = [name[1] for name in CommandsDB.get_all_names_work()] if len(
            CommandsDB.get_all_names_work()) > 0 else False
        if names_work_db:
            await call.message.edit_text(f'Выберите наименование работ\n и нажмите кнопку Продолжить',
                                         reply_markup=KBLines.get_names_one_msg("NAMES", names_work_db))
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


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Выбрать', 'Имя'],
                                                step_menu=['NAMES']),
                           state=[StatesUsers.select_name_work])
async def select_name_work(call: CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get('name_btn') == 'Имя':
        await call.answer(cache_time=1)
    else:
        async with state.proxy() as data:
            data['name_work'] = callback_data.get('name')
        name_work = callback_data.get('name')
        await call.message.edit_text(f'Наименование работы:{"<b>"}{name_work}{"</b>"}\n'
                                     f'Успешно выбрано', reply_markup=KBLines.btn_next_or_back('SEL_NAME'),
                                     parse_mode="HTML")
        await StatesUsers.step_stage_work.set()


################################################
#                   ЭТАПЫ
################################################
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['SEL_NAME']),
                           state=[StatesUsers.step_stage_work, StatesUsers.write_stage_work], )
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['W_STAGE', 'BUILD']),
                           state=[StatesUsers.step_stage_work, StatesUsers.write_stage_work,
                                  StatesUsers.step_build_work], )
async def step_stage(call: CallbackQuery, state: FSMContext):
    await StatesUsers.step_stage_work.set()
    async with state.proxy() as data:
        name_work = data['name_work']
    await call.message.edit_text(f'|     {"<b>"}Форма{"</b>"}      \n'
                                 f'|Наименование работ: {"<b>"}{name_work}{"</b>"}\n'
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
        await call.message.edit_text(f'|     {"<b>"}Форма{"</b>"}\n'
                                     f'|Наименование работ: {"<b>"}{data["name_work"]}{"</b>"}\n'
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
    await call.message.answer(f'|     {"<b>"}Форма{"</b>"}\n'
                              f'|Наименование работ: {"<b>"}{data["name_work"]}{"</b>"}\n'
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
    builds_work_db = [name[1] for name in CommandsDB.get_all_names_builds()] if len(
        CommandsDB.get_all_names_builds()) > 0 else False

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


@dp.callback_query_handler(btn_names_msg.filter(name_btn=['Выбрать', 'Имя'],
                                                step_menu=['BUILDS']),
                           state=[StatesUsers.select_build_work])
async def select_name_work(call: CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get('name_btn') == 'Имя':
        await call.answer(cache_time=1)
    else:
        async with state.proxy() as data:
            data['name_build'] = callback_data.get('name')
        name_build = callback_data.get('name')
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
        await call.message.edit_text(f'|     {"<b>"}Форма{"</b>"}\n'
                                     f'|Наименование работ: {"<b>"}{data["name_work"]}{"</b>"}\n'
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
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить',],
                                                     step_menu=['W_LEVEL',]),
                           state=[StatesUsers.write_level_build_work, ], )
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад', 'Добавить'],
                                                     step_menu=['SEL_WORKER', 'F_WORKERS']),
                           state=[StatesUsers.select_plan_workers, StatesUsers.finish_write_workers], )
async def step_workers(call: CallbackQuery, state: FSMContext):
    await StatesUsers.step_workers.set()
    async with state.proxy() as data:
        if "workers" not in data:
            data['workers'] = {}

        text_msg = f'|     {"<b>"}Форма{"</b>"}\n'\
                   f'|Наименование работ: {"<b>"}{data["name_work"]}{"</b>"}\n'\
                   f'|Этап: {"<b>"}{data["name_stage"]}{"</b>"}\n'\
                   f'|Здание: {"<b>"}{data["name_build"]}{"</b>"}\n'\
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
                           state=[StatesUsers.select_plan_workers, StatesUsers.write_plan_workers,], )
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

@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Продолжить'],
                                                     step_menu=['W_ACTUAL_WORKERS']),
                           state=[StatesUsers.finish_write_workers], )
async def select_write_worker_actually(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text_msg = 'Сотрудники (План/Факт) \n' \
                   '------------------------\n'
        text_msg_end = 'Добавить еще сотрудников?'
        for worker, count in data['workers'].items():
            text_msg = text_msg + f'{"<b>"}{worker} : ({count[0]}/{0 if count[1] is None else count[1]}{"</b>"})\n'
        await call.message.edit_text(text=text_msg + text_msg_end,
                                     reply_markup=KBLines.add_new_worker('F_WORKERS'),
                                     parse_mode='HTML')
        await StatesUsers.finish_write_workers.set()

#####################################
#   sdf
####################################


@dp.callback_query_handler(menu_callback.filter(type_btn=['Добавить']), state=StatesUsers.finish_write_workers)
async def add_new_users(call: CallbackQuery):
    await StatesUsers.step_workers.set()
    await call.message.edit_text('Выберите тип добавляемого сотрудника или \n'
                                 'нажмите кнопку "Пропустить", чтобы продолжить',
                                 reply_markup=get_inline_workers_panel())


@dp.callback_query_handler(menu_callback.filter(type_btn=['Продолжить', 'Пропустить']),
                           state=[StatesUsers.finish_write_workers, StatesUsers.step_workers])
async def next_step(call: CallbackQuery):
    await StatesUsers.step_workers.set()
    await call.message.edit_text('Сохранить форму, или добавить новую строку? \n',
                                 reply_markup=save_form_or_add_string())


def register_handlers_users(dp: Dispatcher):
    ############################
    # Отмена Назад Главное меню
    ############################
    dp.register_message_handler(back_to_user_panel, lambda message: 'Назад' in message.text,
                                state=[StatesUsers.create_new_form,
                                       StatesUsers.write_name_work,
                                       StatesUsers.select_name_work,
                                       StatesUsers.write_stage_work,

                                       ])
    dp.register_message_handler(cmd_users_panel, lambda message: 'Подрядчики' in message.text)
    dp.register_message_handler(create_form, lambda message: 'Создать форму' in message.text,
                                state=StatesUsers.start_user_pamel)

    dp.register_message_handler(select_build_work, lambda message: 'Выбрать Здание' in message.text,
                                state=StatesUsers.step_build_work)

    dp.register_message_handler(write_name_work, state=StatesUsers.write_name_work)
    dp.register_message_handler(write_stage_work, state=StatesUsers.write_stage_work)
    dp.register_message_handler(write_level_build_work, state=StatesUsers.write_level_build_work)
    dp.register_message_handler(write_name_build, state=StatesUsers.write_build_work)
    dp.register_message_handler(write_worker_plan, state=StatesUsers.write_plan_workers)
    dp.register_message_handler(write_worker_actually, state=StatesUsers.write_actually_workers)
