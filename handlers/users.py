from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from create_bot import dp
from keyboards.classic_kb import kb_user_panel, kb_form_name_work, kb_btn_back, kb_build_panel, kb_workers_panel
from memory_FSM.bot_memory import StatesUsers


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
    await message.answer('Выберите следующее шаг ВЫБОР РАБОЧИХ', reply_markup=kb_workers_panel)


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

    dp.register_message_handler(choice_name_work, lambda message: 'Выбрать наименование работ' in message.text,
                                state=StatesUsers.create_new_form)

    # dp.register_message_handler(write_name_work, lambda message: 'Введите наименование работ' in message.text)
    # dp.register_message_handler(choice_name_work, lambda message: 'Выбрать наименование работ' in message.text)
