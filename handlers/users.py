from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from create_bot import dp, bot
from data_base.db_commands import CommandsDB
from keyboards.classic_kb import kb_user_panel, kb_form_name_work, kb_btn_back, kb_build_panel, kb_workers_panel
from memory_FSM.bot_memory import StatesUsers
from keyboards.inlines_kb.kb_inlines import get_inline_workers_panel, get_panel_attempt_add_users, get_btn_add_users, \
    save_form_or_add_string, get_main_menu_user_panel, step_select_or_write_name_work, back_to_main_menu_user, \
    save_name_work, btn_back_menu, get_names_work_one_msg, get_kb_stage, btn_back_names_work, \
    step_select_or_write_build_work, save_name_build, btn_back_builds_work
from keyboards.inlines_kb.callback_datas import workers_callback, menu_callback, add_users, names_work


########################
#      ГЛАВНОЕ МЕНЮ
########################
async def cmd_users_panel(message: types.Message):
    await message.delete()
    await message.answer('Панель управления Подрядчика', reply_markup=get_main_menu_user_panel())
    await StatesUsers.start_user_pamel.set()


@dp.callback_query_handler(menu_callback.filter(type_btn=['Главное меню']),
                           state=[StatesUsers.create_new_form, StatesUsers.write_name_work])
async def back_to_user_panel(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Вы вернулись в меню Подрядчика', reply_markup=get_main_menu_user_panel())
    await state.reset_state()
    await StatesUsers.start_user_pamel.set()


##########################
#     СОЗДАТЬ ФОРМУ
##########################

@dp.callback_query_handler(menu_callback.filter(type_btn=['Создать форму', 'Назад']),
                           state=[StatesUsers.start_user_pamel,
                                  StatesUsers.write_name_work,
                                  StatesUsers.select_name_work])
async def create_form(call: CallbackQuery):
    await StatesUsers.create_new_form.set()
    await call.message.edit_text('Заполнение формы \n Выберите следующий шаг',
                                 reply_markup=step_select_or_write_name_work())


###########################################
#           НАИМЕНОВАНИЯ РАБОТ
###########################################
@dp.callback_query_handler(menu_callback.filter(type_btn=['Добавить работу']),
                           state=[StatesUsers.create_new_form])
async def add_name_work(call: CallbackQuery):
    await call.message.edit_text('Введите наименование работ', reply_markup=None)
    await StatesUsers.write_name_work.set()


@dp.callback_query_handler(menu_callback.filter(type_btn=['Посмотреть наименования', 'Назад'],
                                                btn_menu=['name_work', 'main_menu', 'name_stage']),
                           state=[StatesUsers.create_new_form, StatesUsers.write_name_work,
                                  StatesUsers.step_stage_work])
async def select_name_work(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    names_work_db = [name[1] for name in CommandsDB.get_all_names_work()] if len(
        CommandsDB.get_all_names_work()) > 0 else False
    if names_work_db:
        await call.message.answer(f'Наименования работ: ', reply_markup=get_names_work_one_msg(names_work_db))
        await call.message.answer('Выберите наименование работ для формы \nи нажмите кнопку Продолжить',
                                  reply_markup=btn_back_menu())
        await StatesUsers.select_name_work.set()
    else:
        await call.message.answer('Наименований работ нет.\n'
                                  'Добавьте наименование работ, чтобы продолжить', reply_markup=btn_back_menu(add_btn_next=False))
        await StatesUsers.select_name_work.set()


@dp.callback_query_handler(names_work.filter(type_btn=['Удалить']),
                           state=[StatesUsers.select_name_work])
async def delete_name_work(call: CallbackQuery, callback_data: dict):
    name_work = callback_data.get('name_work')
    if CommandsDB.del_name_work(name_work):
        await call.message.edit_text(f'Наименование работы: {name_work}\n'
                                     f'Успешно удалено', reply_markup=None)
    else:
        await call.message.edit_text(f'Наименование работы: {name_work}\n'
                                     f'Удалить не удалось', reply_markup=None)


@dp.callback_query_handler(names_work.filter(type_btn=['Выбрать', 'Имя']),
                           state=[StatesUsers.select_name_work])
async def select_name_work(call: CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get('type_btn') == 'Имя':
        await call.answer(cache_time=1)
    else:
        async with state.proxy() as data:
            data['name_work'] = callback_data.get('name_work')
        name_work = callback_data.get('name_work')
        await call.message.edit_text(f'Наименование работы: {name_work}\n'
                                     f'Успешно выбрано', reply_markup=None)


async def write_name_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_work'] = message.text
    await message.answer(f'Наименование работы: {data["name_work"]}\n'
                         f'Добавить?',
                         reply_markup=save_name_work())


@dp.callback_query_handler(menu_callback.filter(type_btn=['Добавить']),
                           state=[StatesUsers.write_name_work])
async def add_name_work(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        name_work = data['name_work']
        if CommandsDB.add_name_work(name_work):
            await call.message.edit_text(f'Наименование работы: {name_work}\n'
                                         f'Добавлено', reply_markup=None)
        else:
            await call.message.edit_text(f'Наименование работы: {name_work}\n'
                                         f'Уже есть в базе', reply_markup=None)
    await call.message.answer('Заполнение формы \n Выберите следующий шаг',
                              reply_markup=step_select_or_write_name_work())


################################################
#                   ЭТАПЫ
################################################
@dp.callback_query_handler(menu_callback.filter(type_btn=['Продолжить'], btn_menu=['name_work']),
                           state=[StatesUsers.select_name_work, StatesUsers.write_stage_work], )
@dp.callback_query_handler(menu_callback.filter(type_btn=['Назад'], btn_menu=['name_stage']),
                           state=[StatesUsers.select_name_work, StatesUsers.write_stage_work,
                                  StatesUsers.build_work], )
async def step_stage(call: CallbackQuery, state: FSMContext):
    await StatesUsers.step_stage_work.set()
    async with state.proxy() as data:
        name_work = data['name_work']
    await call.message.edit_text(f'|     {"<b>"}Форма{"</b>"}      \n'
                                 f'|Наименование работ: {name_work}\n'
                                 f'--------------------------------\n'
                                 f'Выберите следующий шаг.',
                                 reply_markup=get_kb_stage(), parse_mode='HTML')


@dp.callback_query_handler(menu_callback.filter(type_btn=['Ввести этап']),
                           state=[StatesUsers.build_work, StatesUsers.step_stage_work])
async def step_write_stage_work(call: CallbackQuery):
    await call.message.edit_text('Введите этап работы', reply_markup=None)
    await StatesUsers.write_stage_work.set()


async def write_stage_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_stage'] = message.text
    await message.delete()
    await message.answer(f"Введенный этап работы: {data['name_stage']} \n"
                         f"Продолжить?", reply_markup=btn_back_names_work())


###################################
#             ЗДАНИЯ
###################################
@dp.callback_query_handler(menu_callback.filter(type_btn=['Продолжить', 'Назад'],
                                                btn_menu=['name_stage']),
                           state=[StatesUsers.write_stage_work, StatesUsers.select_build_work])
async def step_build(call: CallbackQuery, state: FSMContext):
    await StatesUsers.build_work.set()
    async with state.proxy() as data:
        await call.message.edit_text(f'|     {"<b>"}Форма{"</b>"}      \n'
                                     f'|Наименование работ: {data["name_work"]}\n'
                                     f'|Этап: {data["name_stage"]}\n'
                                     f'--------------------------------\n'
                                     f'Выберите следующий шаг.',
                                     reply_markup=step_select_or_write_build_work(), parse_mode='HTML')


@dp.callback_query_handler(menu_callback.filter(type_btn=['Посмотреть здания', 'Назад'],
                                                btn_menu=['name_build']),
                           state=[StatesUsers.build_work, StatesUsers.write_build_work])
async def select_build_work(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    builds_work_db = [name[1] for name in CommandsDB.get_all_names_builds()] if len(
        CommandsDB.get_all_names_builds()) > 0 else False
    print(CommandsDB.get_all_names_builds())
    if builds_work_db:
        await call.message.answer(f'Наименования зданий: ', reply_markup=get_names_work_one_msg(builds_work_db))
        await call.message.answer('Выберите вариант здания для формы \nи нажмите кнопку Продолжить',
                                  reply_markup=btn_back_builds_work())
        await StatesUsers.select_build_work.set()
    else:
        await call.message.answer('Зданий нет.\n'
                                  'Добавьте здание, чтобы продолжить', reply_markup=btn_back_builds_work(add_btn_next=False))
        await StatesUsers.select_build_work.set()


@dp.callback_query_handler(names_work.filter(type_btn=['Удалить']),
                           state=[StatesUsers.select_build_work])
async def delete_build_work(call: CallbackQuery, callback_data: dict):
    name_work = callback_data.get('name_work')
    if CommandsDB.del_name_build(name_work):
        await call.message.edit_text(f'Здание: {name_work}\n'
                                     f'Успешно удалено', reply_markup=None)
    else:
        await call.message.edit_text(f'Здание: {name_work}\n'
                                     f'Удалить не удалось', reply_markup=None)


@dp.callback_query_handler(menu_callback.filter(type_btn=['Добавить здание']),
                           state=[StatesUsers.build_work])
async def add_name_build(call: CallbackQuery):
    await call.message.edit_text('Введите наименование здания', reply_markup=None)
    await StatesUsers.write_build_work.set()


async def write_name_build(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_build'] = message.text
    await message.answer(f'Наименование здания: {data["name_build"]}\n'
                         f'Добавить?',
                         reply_markup=save_name_build())


@dp.callback_query_handler(menu_callback.filter(type_btn=['Добавить'], btn_menu=['name_build']),
                           state=[StatesUsers.write_build_work])
async def add_name_build(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    async with state.proxy() as data:
        name_build = data['name_build']
        if CommandsDB.add_name_build(name_build):
            await call.message.edit_text(f'Наименование здания: {name_build}\n'
                                         f'Добавлено', reply_markup=None)
        else:
            await call.message.edit_text(f'Наименование здания: {name_build}\n'
                                         f'Уже есть в базе', reply_markup=None)
    await call.message.answer(f'|     {"<b>"}Форма{"</b>"}      \n'
                              f'|Наименование работ: {data["name_work"]}\n'
                              f'|Этап: {data["name_stage"]}\n'
                              f'--------------------------------\n'
                              f'Выберите следующий шаг.',
                              reply_markup=step_select_or_write_build_work(), parse_mode='HTML')
    await StatesUsers.build_work.set()


################################################################


async def step_write_build_work(message: types.Message):
    await StatesUsers.write_build_work.set()
    await message.answer('Введите наименование здания', reply_markup=kb_btn_back)


#
# async def write_build_work(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['name_build'] = message.text
#     await message.answer('Введите этаж', reply_markup=kb_btn_back)
#     await StatesUsers.write_level_build_work.set()


#################################
#    РАБОЧИЕ ИТР ОХРАНА
#################################
async def write_level_build_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['level_build_work'] = message.text
    await StatesUsers.step_workers.set()
    await message.answer('Выберите тип добавляемого сотрудника или \n'
                         'нажмите кнопку "Пропустить", чтобы продолжить', reply_markup=get_inline_workers_panel())


@dp.callback_query_handler(workers_callback.filter(type_step='workers'), state=StatesUsers.step_workers)
async def select_security(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        if not data.get(callback_data['type_worker'] + '_план'):
            data['actual_user'] = callback_data['type_worker']
            data['actual_user_plan'] = callback_data['type_worker'] + '_план'
            data[data['actual_user_plan']] = 0
            await call.answer(cache_time=20)
            # await call.message.edit_reply_markup(reply_markup=None)
            await call.message.edit_text(f"Выбран тип сотрудника: {data['actual_user']}\n"
                                         f"Планируемое количество: 0\n"
                                         f"Фактическое количество: 0\n"
                                         f"Введите планируемое количество сотрудников",
                                         reply_markup=get_btn_add_users())
            await StatesUsers.write_plan_workers.set()


async def update_number_plan(message: types.Message, state: FSMContext, new_value: int):
    async with state.proxy() as data:
        await message.edit_text(f"Выбран тип сотрудника: {data['actual_user']}\n"
                                f"Планируемое количество: {new_value}\n"
                                f"Фактическое количество: 0\n"
                                f"Введите планируемое количество сотрудников", reply_markup=get_btn_add_users())
        await StatesUsers.write_plan_workers.set()


async def update_number_actually(message: types.Message, state: FSMContext, new_value: int):
    async with state.proxy() as data:
        await message.edit_text(f"Выбран тип сотрудника: {data['actual_user']}\n"
                                f"Планируемое количество: {data[data['actual_user_plan']]}\n"
                                f"Фактическое количество: {new_value}\n"
                                f"Введите фактическое количество сотрудников", reply_markup=get_btn_add_users())
        await StatesUsers.write_actually_workers.set()


@dp.callback_query_handler(add_users.filter(type_btn=['plus', 'minus']),
                           state=[StatesUsers.write_plan_workers, StatesUsers.step_workers])
async def write_plan_user(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        action = callback_data.get('type_btn')
        if action == "plus":
            number = int(callback_data.get('type'))
            data[data['actual_user_plan']] = data[data['actual_user_plan']] + number
            await update_number_plan(call.message, state, data[data['actual_user_plan']])
        elif action == 'minus':
            number = int(callback_data.get('type'))
            data_number = data[data['actual_user_plan']]
            if data_number - number >= 0:
                data[data['actual_user_plan']] = data_number - number
                await update_number_plan(call.message, state, data[data['actual_user_plan']])
            else:
                await call.answer(cache_time=1)


@dp.callback_query_handler(add_users.filter(type_btn=['plus', 'minus']),
                           state=[StatesUsers.write_actually_workers])
async def write_actually_user(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        action = callback_data.get('type_btn')
        if action == "plus":
            number = int(callback_data.get('type'))
            data[data['actual_user_actually']] = data[data['actual_user_actually']] + number
            await update_number_actually(call.message, state, data[data['actual_user_actually']])
        elif action == 'minus':
            number = int(callback_data.get('type'))
            data_number = data[data['actual_user_actually']]
            if data_number - number >= 0:
                data[data['actual_user_actually']] = data_number - number
                await update_number_actually(call.message, state, data[data['actual_user_actually']])
            else:
                await call.answer(cache_time=1)


@dp.callback_query_handler(add_users.filter(type_btn=['Подтвердить']),
                           state=[StatesUsers.write_plan_workers])
async def write_actually_user(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await StatesUsers.write_actually_workers.set()
    async with state.proxy() as data:
        data['actual_user_actually'] = data['actual_user'] + '_актуально'
        data[data['actual_user_actually']] = 0
        await call.answer(cache_time=1)
        await call.message.edit_text(f"Выбран тип сотрудника: {data['actual_user']}\n"
                                     f"Планируемое количество: {data[data['actual_user_plan']]}\n"
                                     f"Фактическое количество: {0}\n"
                                     f"Введите фактическое количество сотрудников", reply_markup=get_btn_add_users())


# async def write_plan_workers(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['workers_plan'] = message.text
#         for key, value in data.items():
#             print(key, value)
#     await message.answer('Введите фактическое количество сотрудников')
#     await StatesUsers.write_actually_workers.set()

@dp.callback_query_handler(add_users.filter(type_btn=['access']),
                           state=[StatesUsers.write_actually_workers])
async def write_actually_workers(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await call.message.edit_text(f"Выбран тип сотрудника: {data['actual_user']}\n"
                                     f"Планируемое количество: {data[data['actual_user_plan']]}\n"
                                     f"Фактическое количество: {data[data['actual_user_actually']]}\n",
                                     reply_markup=None)
        await call.message.answer("Добавить еще сотрудников?\n", reply_markup=get_panel_attempt_add_users())
        await StatesUsers.finish_write_workers.set()


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


async def select_build_work(message: types.Message):
    builds = ['Здание1', 'Здание2']
    await StatesUsers.select_build_work.set()
    for build in builds:
        await message.answer(f'{build}',
                             reply_markup=types.InlineKeyboardMarkup(row_width=1).
                             add(types.InlineKeyboardButton(text='Выбрать', callback_data=f'{build}')))
    await message.answer('Выберите здание для формы', reply_markup=kb_btn_back)


async def choice_name_work(message: types.Message):
    await StatesUsers.select_name_work.set()
    for i in range(1, 2):
        await message.answer(f'Наименование работы,\n наименование: {i}',
                             reply_markup=types.InlineKeyboardMarkup(row_width=1).
                             add(types.InlineKeyboardButton(text=f'Выбрать', callback_data=f'nw_{i}')))
    await message.answer("Выберите наименование работ, \n или вернитесь Назад", reply_markup=kb_btn_back)


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
    # dp.register_message_handler(back_to_admin_panel, lambda message: 'Отменить' in message.text,
    #                             state=[StatesAdminUser.write_user_comment])
    # dp.register_message_handler(back_to_admin_panel, lambda message: 'В главное меню' in message.text,
    #                             state=[StatesAdminUser.save_user])

    dp.register_message_handler(cmd_users_panel, lambda message: 'Подрядчики' in message.text)
    dp.register_message_handler(create_form, lambda message: 'Создать форму' in message.text,
                                state=StatesUsers.start_user_pamel)
    dp.register_message_handler(add_name_work, lambda message: 'Ввести наименование работ' in message.text,
                                state=StatesUsers.create_new_form)

    dp.register_message_handler(step_write_build_work, lambda message: 'Добавить Здание' in message.text,
                                state=StatesUsers.build_work)
    dp.register_message_handler(select_build_work, lambda message: 'Выбрать Здание' in message.text,
                                state=StatesUsers.build_work)

    dp.register_message_handler(write_name_work, state=StatesUsers.write_name_work)
    dp.register_message_handler(write_stage_work, state=StatesUsers.write_stage_work)

    dp.register_message_handler(write_name_build, state=StatesUsers.write_build_work)
    dp.register_message_handler(write_level_build_work, state=StatesUsers.write_level_build_work)
    dp.register_message_handler(write_actually_workers, state=StatesUsers.write_actually_workers)

    dp.register_message_handler(choice_name_work, lambda message: 'Выбрать наименование работ' in message.text,
                                state=StatesUsers.create_new_form)
