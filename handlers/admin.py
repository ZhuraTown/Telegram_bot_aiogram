from aiogram import types, Dispatcher
from keyboards.classic_kb import kb_admin_panel, kb_get_table_panel
from aiogram.dispatcher import FSMContext

from memory_FSM.bot_memory import StatesAdmin
from create_bot import dp


async def cmd_admin_panel(message: types.Message):
    await message.answer('Панель управления Ген подрядчика', reply_markup=kb_admin_panel)


async def get_table(message: types.Message):
    await message.answer('Выгрузка таблицы', reply_markup=kb_get_table_panel)
    await StatesAdmin.admin_table_menu.set()


async def back_to_admin_panel(message: types.Message, state: FSMContext):
    await message.answer('Вы вернулись в основное меню администратора', reply_markup=kb_admin_panel)
    await state.reset_state()

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cmd_admin_panel, lambda message: 'Ген_подрядчик' in message.text)
    dp.register_message_handler(get_table, lambda message: 'Выгрузить таблицу' in message.text)
    dp.register_message_handler(back_to_admin_panel, lambda message: 'Назад' in message.text, state=[StatesAdmin.admin_table_menu])
