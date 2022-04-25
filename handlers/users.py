from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from create_bot import dp
from keyboards.classic_kb import kb_user_panel, kb_form_name_work, kb_btn_back, kb_build_panel, kb_workers_panel
from memory_FSM.bot_memory import StatesUsers
from keyboards.inlines_kb.kb_inlines import get_inline_workers_panel, get_panel_attempt_add_users, get_btn_add_users
from keyboards.inlines_kb.callback_datas import workers_callback, menu_callback, add_users


########################
#      ГЛАВНОЕ МЕНЮ
########################
async def cmd_users_panel(message: types.Message):
    await message.delete()
    await message.answer('Панель управления Подрядчика', reply_markup=kb_user_panel)
    await StatesUsers.start_user_pamel.set()


async def back_to_user_panel(message: types.Message, state: FSMContext):
    await message.answer('Вы вернулись в меню Подрядчика', reply_markup=kb_user_panel)
    await state.reset_state()
    await StatesUsers.start_user_pamel.set()


##########################
#     СОЗДАТЬ ФОРМУ
##########################


async def create_form(message: types.Message):
    await message.answer('Заполнение формы \n Выберите следующий шаг', reply_markup=kb_form_name_work)
    await StatesUsers.create_new_form.set()


async def add_name_work(message: types.Message):
    await message.delete()
    await message.answer('Введите наименование работ', reply_markup=kb_btn_back)
    await StatesUsers.write_name_work.set()


async def write_name_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_work'] = message.text
    await message.answer('Введите этап', reply_markup=kb_btn_back)
    await StatesUsers.write_stage_work.set()


###########################
#    ВЫБОР ДОБАВИТЬ ЗДАНИЯ ВВЕСТИ
###########################
async def write_stage_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_stage'] = message.text
    await message.answer('Выберите следующий шаг ЗДАНИЯ', reply_markup=kb_build_panel)
    await StatesUsers.build_work.set()


async def step_write_build_work(message: types.Message):
    await StatesUsers.write_build_work.set()
    await message.answer('Введите наименование здания ПОМЕТОЧКА', reply_markup=kb_btn_back)


async def write_build_work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_build'] = message.text
    await message.answer('Введите этаж', reply_markup=kb_btn_back)
    await StatesUsers.write_level_build_work.set()


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
async def select_security(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(f"Выбран тип сотрудника: {callback_data['type_worker']}\n"
                              f"Введите планируемое количество сотрудников")
    await StatesUsers.write_plan_workers.set()


async def write_plan_workers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['workers_plan'] = message.text
    await message.answer('Введите фактическое количество сотрудников')
    await StatesUsers.write_actually_workers.set()


async def write_actually_workers(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['workers_actually'] = message.text
    await message.answer("Добавить еще сотрудников?\n", reply_markup=get_panel_attempt_add_users())
    await StatesUsers.finish_write_workers.set()

# async def write_actually_workers_update(message: types.Message, new_value: list):
#     with suppress(MessageNotModified):
#         await message.edit_text(f'\t          \tПлан | Факт \n'
#                                 f'\tОхрана:   \t   {new_value[0]} |  0 \n'
#                                 f'\tДежурный: \t   {new_value[1]} |  0 \n'
#                                 f'\tРабочий:  \t   {new_value[2]} |  0 \n'
#                                 f'\tИТР:      \t   {new_value[3]} |  0', reply_markup=get_btn_add_users())
#
#
# async def write_actually_workers(message: types.Message):
#     await message.edit_text(f'\t          \tПлан | Факт \n'
#                             f'\tОхрана:   \t   0 |  0 \n'
#                             f'\tДежурный: \t   0 |  0 \n'
#                             f'\tРабочий:  \t   0 |  0 \n'
#                             f'\tИТР:      \t   0 |  0', reply_markup=get_btn_add_users())


# @dp.callback_query_handler(add_users.filter(), state=StatesUsers.finish_write_workers)
# async def edit_count_users(call: CallbackQuery, callback_data: dict):
#     await call.answer(cache_time=60)
#     await call.answer(f'\t          \tПлан | Факт \n\t'
#                          f'\tОхрана:   \t   0 |  0 \n'
#                          f'\tДежурный: \t   0 |  0 \n'
#                          f'\tРабочий:  \t   0 |  0 \n'
#                          f'\tИТР:      \t   0 |  0',)


# @dp.callback_query_handler(menu_callback.filter(type_btn='Добавить'), state=StatesUsers.finish_write_workers)
# async def add_new_user()


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
    dp.register_message_handler(write_build_work, state=StatesUsers.write_build_work)
    dp.register_message_handler(write_level_build_work, state=StatesUsers.write_level_build_work)
    dp.register_message_handler(write_plan_workers, state=StatesUsers.write_plan_workers)
    dp.register_message_handler(write_actually_workers, state=StatesUsers.write_actually_workers)

    dp.register_message_handler(choice_name_work, lambda message: 'Выбрать наименование работ' in message.text,
                                state=StatesUsers.create_new_form)

    # dp.register_message_handler(write_name_work, lambda message: 'Введите наименование работ' in message.text)
    # dp.register_message_handler(choice_name_work, lambda message: 'Выбрать наименование работ' in message.text)
