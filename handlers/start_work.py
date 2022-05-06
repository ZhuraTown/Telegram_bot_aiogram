from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data_base.db_commands import CommandsDB
from keyboards.classic_kb import kb_start, kb_admin_panel, kb_user_panel
from keyboards.inlines_kb.callback_datas import menu_callback_user
from keyboards.inlines_kb.kb_inlines import KBLines
from memory_FSM.bot_memory import StatesAdminUser, AuthorizationUser, StatesUsers
from create_bot import dp, bot


async def command_start(message: types.Message, state: FSMContext):
    await message.delete()
    await state.reset_state()
    await message.answer('Цель бота, упростить заполнение табеля рабочего времени сотрудников Лахта Центр\n'
                         'Введите PIN_CODE для входа в личный кабинет', reply_markup=None)
    await AuthorizationUser.write_password.set()


@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Выйти'],
                                                     step_menu=['Step_MAIN']),
                           state=[StatesUsers.start_user_pamel])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Выйти'],
                                                     step_menu=['ADMIN_PANEL']),
                           state=[StatesAdminUser.start_admin_panel])
@dp.callback_query_handler(menu_callback_user.filter(name_btn=['Назад'],
                                                     step_menu=['AUTH_ADMIN', 'AUTH_USER']),
                           state=[AuthorizationUser.correct_password_admin,
                                  AuthorizationUser.correct_password_user])
async def command_start_back(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.message.edit_text('Вы вернулись в стартовое меню\n'
                                 'Цель бота, упростить заполнение табеля рабочего времени сотрудников Лахта Центр\n'
                                 'Введите PIN_CODE для входа в личный кабинет', reply_markup=None)
    await AuthorizationUser.write_password.set()


async def authorization_step(message: types.Message, state: FSMContext):
    pin_cods = CommandsDB.get_all_users(user_password=True)
    msg = message.text
    if msg in pin_cods:
        async with state.proxy() as data:
            if pin_cods[msg][1]:
                await message.delete()
                await message.answer(
                    f'Введён верный PINCODE\nВы хотите продолжить как:{"<b>"}{pin_cods[msg][0]}{"</b>"}?\n'
                    f'Пользователь владеет правами {"<b>"}Администратора{"</b>"}.\n'
                    f'Он может добавлять/удалять пользователей, получать полный отчёт о работах.\n'
                    f'Нажмите кнопку {"<b>"}Продолжить{"</b>"}, чтобы приступить к работе.\n'
                    f'Кнопку {"<b>"}Назад{"</b>"}, чтобы вернуться к вводу пароля',
                    parse_mode='HTML', reply_markup=KBLines.btn_next_or_back('AUTH_ADMIN'))
                data['user_name'] = pin_cods[msg][0]
                await AuthorizationUser.correct_password_admin.set()

            else:
                await message.delete()
                await message.answer(
                    f'Введён верный PINCODE\nВы хотите продолжить как: {"<b>"}{pin_cods[msg][0]}{"</b>"}?\n'
                    f'Данный пользователь может добавлять/редактировать/удалять формы своей компании.\n'
                    f'Нажмите кнопку {"<b>"}Продолжить{"</b>"}, чтобы приступить к работе.\n'
                    f'Кнопку {"<b>"}Назад{"</b>"}, чтобы вернуться к вводу пароля',
                    parse_mode='HTML', reply_markup=KBLines.btn_next_or_back('AUTH_USER'))
                data['user_name'] = pin_cods[msg][0]
                await AuthorizationUser.correct_password_user.set()
    else:
        await message.answer('Такого PINCODE нету в системе. Уточните свой пароль')


async def command_help(message: types.Message):
    await message.answer('ПОМОЩЬ ПОДСКАЗКИ')


def register_handlers_start_work(dp: Dispatcher):
    dp.register_message_handler(command_start, lambda message: 'Выйти' in message.text,
                                state=[StatesAdminUser.start_admin_panel])
    dp.register_message_handler(authorization_step, state=[AuthorizationUser.write_password])
    dp.register_message_handler(command_start, commands=['start'], state=None)
    dp.register_message_handler(command_start, commands=['start'], state=[AuthorizationUser.write_password])
    dp.register_message_handler(command_help, commands=['help'], state='*')
