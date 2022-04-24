from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from keyboards.classic_kb import kb_start, kb_admin_panel, kb_user_panel
from memory_FSM.bot_memory import StatesAdminUser
from create_bot import dp, bot


async def command_start(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer('Цель бота, упростить заполнение табеля рабочего времени сотрудников Лахта Центр\n'
                         'Введите PIN_CODE для входа в личный кабинет', reply_markup=kb_start)
    await state.reset_state()


async def command_help(message: types.Message):
    await message.answer('ПОМОЩЬ ПОДСКАЗКИ')


def register_handlers_start_work(dp: Dispatcher):
    dp.register_message_handler(command_start, lambda message: 'Выйти' in message.text,
                                state=[StatesAdminUser.start_admin_panel])
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])


