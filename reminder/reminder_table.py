import asyncio
import datetime

from data_base.db_commands import CommandsDB
from aiogram import Bot
from aiogram.utils.exceptions import ChatNotFound

# """ Напоминатель по заполнению табеля времени
#  WEEKEND - дни недели без проверок(сб и вс)
#  TIME_REMIND_H - час напоминания
#  TIME_REMIND_START_M - минуты для напоминания
#  TIME_REMIND_FINISH_M - минуты для напоминания
#  """
# WEEKEND = [5, 6]
# TIME_REMIND_START_M = 0
# TIME_REMIND_FINISH_M = 45
# TIME_REMIND_H = 9
# DELAY = 60


async def remind_fill_out_form(bot: Bot, message: str):
    """ Напоминть пользователем заполнить работу """
    chat_ids = CommandsDB.get_users_with_chat_id_is_remind(is_remind=True)
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id[0],
                                   text=f"{'<b>'}{message}{'</b>'}",
                                   parse_mode='HTML')
        except ChatNotFound:
            print(f'Чат не нашел, искал {chat_id}')


async def del_remind_fill_out_form():
    """ Обнулить напоминание пользователем. В 23.30 выставлять всем пользователем напоминание """
    chat_ids = CommandsDB.get_users_with_chat_id_is_remind(is_remind=False)
    for chat_id in chat_ids:
        CommandsDB.change_state_reminder_chat_id(chat_id[0], is_remind=True)
